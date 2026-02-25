gokuu = {
    "かめはめ波": True,
    "ファイナルフラッシュ": False,
    "サイヤ人": True,
}

vegita = {
    "かめはめ波": False,
    "ファイナルフラッシュ": True,
    "サイヤ人": True,
}

skills = ["かめはめ波", "ファイナルフラッシュ", "サイヤ人"]

gojita = {}

for skill in skills:
    if gokuu[skill] and vegita[skill]:
        gojita[skill] = True
    elif gokuu[skill] or vegita[skill]:
        gojita[skill] = True
    else:
        gojita[skill] = False

print(gojita)


