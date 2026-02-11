import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

# Markdown: ![alt](path)
MD_IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
# HTML: <img src="..."> or <img ... src='...'>
HTML_IMG_RE = re.compile(r'(<img\b[^>]*?\bsrc=)(["\'])(.*?)\2', re.IGNORECASE)

def sh(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()

def get_github_owner_repo() -> str:
    url = sh(["git", "config", "--get", "remote.origin.url"])
    m = re.search(r'github\.com[:/](.+?)/(.+?)(?:\.git)?$', url)
    if not m:
        raise RuntimeError(f"Unsupported origin url: {url}")
    return f"{m.group(1)}/{m.group(2)}"

def get_branch() -> str:
    return sh(["git", "rev-parse", "--abbrev-ref", "HEAD"])

def build_filename_index(repo_root: Path) -> dict[str, str]:
    """
    repo内の全ファイルを走査して {filename: repo内相対パス} を作る。
    同名が複数あったら最初に見つかったものを採用（簡易）。
    """
    index: dict[str, str] = {}
    for p in repo_root.rglob("*"):
        if p.is_file():
            name = p.name
            if name not in index:
                index[name] = p.relative_to(repo_root).as_posix()
    return index

def is_http_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")

def extract_filename(path_or_url: str) -> str | None:
    """
    ./img/a.png?x=1 -> a.png
    a.png -> a.png
    https://.../a.png -> a.png (ただし置換対象にはしない想定)
    """
    # クエリやフラグメント除去
    base = path_or_url.split("#", 1)[0].split("?", 1)[0].strip()
    if not base:
        return None
    # URLっぽい場合もファイル名は取れるが、置換はしない運用
    parsed = urlparse(base)
    if parsed.scheme in ("http", "https"):
        return Path(parsed.path).name or None
    return Path(base).name or None

def replace_images_by_filename(markdown: str) -> str:
    repo_root = Path(sh(["git", "rev-parse", "--show-toplevel"]))
    owner_repo = get_github_owner_repo()
    branch = get_branch()
    index = build_filename_index(repo_root)

    def to_raw_url(filename: str) -> str | None:
        rel = index.get(filename)
        if not rel:
            return None
        return f"https://raw.githubusercontent.com/{owner_repo}/{branch}/{rel}"

    # 1) Markdown記法の置換
    def md_repl(m):
        alt = m.group(1)
        target = m.group(2).strip()
        if is_http_url(target):
            return m.group(0)

        fn = extract_filename(target)
        if not fn:
            return m.group(0)

        url = to_raw_url(fn)
        if not url:
            return m.group(0)

        return f"![{alt}]({url})"

    markdown = MD_IMG_RE.sub(md_repl, markdown)

    # 2) HTML <img> の置換
    def html_repl(m):
        prefix = m.group(1)     # '<img ... src=' まで
        quote = m.group(2)      # ' or "
        target = m.group(3).strip()
        if is_http_url(target):
            return m.group(0)

        fn = extract_filename(target)
        if not fn:
            return m.group(0)

        url = to_raw_url(fn)
        if not url:
            return m.group(0)

        return f"{prefix}{quote}{url}{quote}"

    markdown = HTML_IMG_RE.sub(html_repl, markdown)

    return markdown
