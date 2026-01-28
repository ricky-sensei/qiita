import requests
import json
import datetime
import pytz

BASE_URL = "https://qiita.com/api/v2/items"

def putQiitaArticle(title, markdown, path="article", id=""):
    token = "ベアラートークンを発行してください。"
    headers = {"Authorization": f"Bearer {token}"}
    item = {
        "title": title,
        "id": id,
        "tags": [
            {
            "name": "qiita"
            },
            {
            "name": "test"
            }
        ],
        "private": False,
        "coediting": False,
        "tweet": False,
        "body": markdown
    }
    # idがなければ、新規で記事を投稿
    if item["id"] == "":
        res = requests.post(BASE_URL, headers=headers, json=item)
        return res
    else:
        now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        item["title"] += now.strftime("【%Y/%m/%d %H時更新】")
        item_id = item["id"]
        res = requests.patch(BASE_URL + f"/{item_id}", headers=headers, json=item)
        return res
