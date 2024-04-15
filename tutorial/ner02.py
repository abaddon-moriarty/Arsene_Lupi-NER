import json


with open("./books/Arsène_Lupin_gentleman-cambrioleur.txt", "r", encoding="utf-8") as f:
    text = f.read().split("\n\n")[50:60]
    # print(text)

alias_extended = []
skip = ["de", "Le", "M."]
with open("./tutorial/data/alias.json", "r", encoding="utf-8") as f:
    alias = json.load(f)
    # print(alias)
    for al in alias:
        names = al.split()
        for name in names:
            if name not in skip:
                alias_extended.append(name)

print(alias_extended)
        


for segment in text:
    segment = segment.strip().replace("\n", " ")
    # print(segment)

    punkt = "!\"#$%&'()*+,./:;<=>?@[\]^_`{|}~«»…"
    for ele in segment:
        if ele in punkt:
            segment = segment.replace("-", " ")
            segment = segment.replace(ele, "").replace("  ", " ") # this remove any punctuation in the list from the string
    # print(segment)
    words = segment.split()
    # print(words)

    i=0
    for word in words:
        if word in alias_extended:
            if words[i-1][0].isupper():
                print(f"alias found: {words[i-1][0]} {word}")
            else:
                print(f"alias found: {word}")
        i = i+1