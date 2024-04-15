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

# print(alias_extended)
        
total = 0

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
    print(segment)

    for word in words:
        i = words.index(word)
        if word in alias_extended:
            # Only check if the following word is not also an alias, to to avoid counting "Arsène" and "Arsène Lupin" as two entities. it will skip this word then
            if words[i+1] not in alias_extended: 
                # if the word before starts with an uppercase, counts as Mr
                if words[i-1][0].isupper():
                    # print(f"Alias is: {word}, previous word is: {words[i-1]}")
                    print(f"Alias found: {words[i-1]} {word}")
                    total += 1
                else:
                    print(f"Alias found: {word}")
                    total += 1

print(f"Total entities: {total}")