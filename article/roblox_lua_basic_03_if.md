# Roblox Lua 基礎③  
# if文（条件分岐）

------------------------------------------------------------------------

## 🎯 今日の目標

- 条件によって処理を分けられるようになる  
- if / elseif / else の書き方を覚える  
- ゲームでよくある「判定」を作れるようになる  

------------------------------------------------------------------------

# 1. if文ってなに？

**if文** は、  
「もし〜だったら、これをする」という処理を書くための仕組み。

ゲームの中では、こんな場面で使われている。

- HPが0になったらゲームオーバー  
- スコアが100点以上ならクリア  
- カギを持っていたらドアが開く  

---

# 2. if文の基本の形

```lua
if 条件 then
    条件がtrueのときに実行される
end
```

例：

```lua
local hp = 0

if hp <= 0 then
    print("ゲームオーバー")
end
```

条件が **true** のときだけ、中の処理が実行される。

------------------------------------------------------------------------

# 3. if / else

「そうじゃなかったら」を書くこともできる。

```lua
local hp = 50

if hp <= 0 then
    print("ゲームオーバー")
else
    print("まだ生きている")
end
```

---

# 4. if / elseif / else

条件がたくさんあるときは `elseif` を使う。

```lua
local score = 85

if score >= 100 then
    print("Sランク")
elseif score >= 80 then
    print("Aランク")
elseif score >= 60 then
    print("Bランク")
else
    print("Cランク")
end
```

上から順番に条件がチェックされ、  
最初に true になったところだけが実行される。

------------------------------------------------------------------------

# 5. 比較演算子・論理演算子と一緒に使う

第2章で学んだ内容を組み合わせると、  
ゲームらしい判定が作れる。

```lua
local hp = 30
local hasKey = true

if hp > 0 and hasKey then
    print("ドアが開いた")
else
    print("ドアは開かない")
end
```

---

# 6. よくあるミス

### ❌ then を忘れる

```lua
-- ダメな例
if hp <= 0
    print("ゲームオーバー")
end
```

### ✅ 正しい書き方

```lua
if hp <= 0 then
    print("ゲームオーバー")
end
```

---

### ❌ end を忘れる

if文は **必ず end で閉じる** 必要がある。

------------------------------------------------------------------------

# 7. 出力を予想してみよう

次のコードを実行すると、何が表示される？

```lua
local hp = 40
local damage = 30

hp = hp - damage

if hp <= 0 then
    print("ゲームオーバー")
elseif hp < 50 then
    print("ピンチ！")
else
    print("まだ余裕")
end
```

<details><summary>答え</summary>

```
ピンチ！
```

</details>

------------------------------------------------------------------------

# 8. Roblox Studioでやってみよう

触れたらメッセージが変わるブロックを作ってみよう。

```lua
local part = script.Parent

local function onTouched(hit)
    local character = hit.Parent
    if not character then return end

    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if not humanoid then return end

    if humanoid.Health <= 0 then
        print("すでにゲームオーバー")
    elseif humanoid.Health < 50 then
        print("HPが少ない！")
    else
        print("まだ元気")
    end
end

part.Touched:Connect(onTouched)
```

------------------------------------------------------------------------

# 9. まとめ

- if文で条件によって処理を分けられる  
- true / false がとても大事  
- 比較演算子・論理演算子とセットで使う  
- ゲームの「判定」はほぼ if文  

------------------------------------------------------------------------

# 🎮 ミニチャレンジ

1. HPが100以上なら「満タン」と表示しよう  
2. スコアによってランクを3段階で表示しよう  
3. HPが0以下のときだけダメージを受けないようにしてみよう  
