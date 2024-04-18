import os
import json

        
def aliasRecognition(segments, result):
    total = 0

    for segment in segments:
        words = segment.split()
        
        for word in words:
            i = words.index(word)
            if word in alias_extended:
                print(f"Maybe found: {word}")
                result.write(f"\t{segment}\n")
                result.write(f"\nMaybe found: {word}\n")

                # Only check if the following word is not also an alias, to avoid counting "Arsène" and "Arsène Lupin" as two entities. 
                # if next word exists and next word not in alias_extended
                if (i+1 < len(words)) and (words[i+1] not in alias_extended): # this ensures that we don't get an out of index error                   
                        # if previous word starts with uppercase
                        if words[i-1][0].isupper():
                            # print(f"Alias is: {word}, previous word is: {words[i-1]}")
                            print(f"Alias found: {words[i-1]} {word}")
                            result.write(f"\nAlias found: {words[i-1]} {word}\n")
                            total += 1
                else:
                    print(f"Alias found: {word}")
                    result.write(f"\nAlias found: {word}\n")

                    total += 1


    print(f"Total entities: {total}")
    result.write(f"\nTotal entities found: {total}\n\n\n\n\n\n")

def preprocessing(text):
    segments = []
    for segment in text:
        segment = segment.strip().replace("\n", " ")
        # print(segment)

        punkt = "!\"#$%&'’()*+,./:;<=>?@[\]^_`{|}~«»…"
        for ele in segment:
            if ele in punkt:
                segment = segment.replace("-", " ").replace("’", " ")
                segment = segment.replace(ele, "").replace("  ", " ") # this remove any punctuation in the list from the string
        segments.append(segment)
    return segments
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

with open("./tutorial/results.txt", "w", encoding="utf-8") as result:
    all_books = os.listdir("./books/")
    for bookname in all_books[:1]:
        print (bookname)
        with open("./books/" + bookname , mode='r', encoding='utf-8') as f:
            book = f.read().split("\n\n")
            segments = preprocessing(book)
            result.write(f"Book name: {bookname}\n\n\n")
            aliasRecognition(segments, result)

        
