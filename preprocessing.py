import os
import re
from tqdm import tqdm

def remove_paratext(book, recap, bookname):

    remove = ["↑", "⁂", "* * *"]
    segments = []

    # print("\nremoving paratext\n")
    end = book.find("À propos de cette édition électronique") # This removes the end paratext from Wiki
    beginning = book.find("TABLE DES MATIÈRES") # This removes the paratext found at the beginning. Still need to work on table of content though

    if beginning:
        recap[bookname]["paratext"] = [book[:beginning], book[end:]]
        book = book[beginning:end].split("\n\n")
    else:
        beginning = book.find("Exporté de Wikisource") # This removes the paratext found at the beginning. Still need to work on table of content though
        print(book[:beginning])
        recap[bookname]["paratext"] = [book[end:]]
        book = book[:end].split("\n\n")

    for segment in book:
        segment = segment.strip()
        if segment: #removing empty items
            for item in remove: # checks if the line doesn't have a symbol we want to remove
                if item in segment:
                    if item in recap:
                        recap[bookname][item].append(segment)
                        break
                    else:
                        recap[bookname][item] = [segment]
                        break
            else:
                segments.append(segment.strip())
            if re.search("\[.*\]", segment):
                segment = re.sub("\[.*\]", "", segment) # Equivalent of String.replace("x, "y")
                # print(segment)
                segments.append(segment.strip())

    return segments

def remove_letterine(segments, log):

    mods = 0
    no_match = []
    punkt = "!\"#$%&'’()*+,./:;<=>?@[\\]^_`{|}~«»… ⁂"


    for i, segment in tqdm(enumerate(segments), desc="Processing segment"):
        index = 0
        if len(segment) == 1 & i < len(segments) - 1: # If there's only one char in the line
            while segments[i+1][index] in punkt: # This should skip the punctuation and spaces
                index = index + 1
            if segments[i+1][index].islower(): # Checks if the first letter of the next line is lowercase. 
                log.write(f"The lines: {segments[i]}     {segments[i+1][:50]} [...] were merged.\n")
                segments[i] = segments[i] + segments[i+1]
                segments.pop(i+1)
                mods +=1
            else:
                no_match.append([segments[i], segments[i+1]])
    return segments, mods, no_match

modifs = []
recap = {}



root = "C:\\Users\\munau\\OneDrive\\Desktop\\Machine_Learning\\Arsène Lupin Project\\Arsene_Lupi-NER\\"
book_dir = f"{root}books\\"

x = 1
while os.path.exists(f"C:\\Users\\munau\\OneDrive\\Desktop\\Machine_Learning\\Arsène Lupin Project\\Arsene_Lupi-NER\\log\\preprocessing_{x}.log"):
    x = x + 1

for bookname in tqdm(os.listdir(book_dir), desc="Processing Book"):

    norm_text = []

    norm_name = f"{root}input\\{bookname[:-4]}_norm{bookname[-4:]}"
    log = open(f"{root}log\\preprocessing_{x}.log", "a", encoding='utf-8')
    f = open(os.path.join(book_dir, bookname), "r", encoding='utf-8')
    norm = open(f"{root}input\\{bookname[:-4]}_norm{bookname[-4:]}", "w", encoding='utf-8')


    log.write(f"Pre-processing the book: {bookname}.\n")
    # print(f"Pre-processing the book: {bookname}.\n")
    recap[bookname] = {}
    book = f.read()
    segments = remove_paratext(book, recap, bookname)

    segments, mods, no_match = remove_letterine(segments, log)
    
    for line in segments:
        norm.write(f"{line}\n")
            
    # print(f"in the book: \"{bookname}\", {mods} lines were modified.\n")
    if no_match:
        log.write(f"Total of {mods} line merges were made.\nThe following lines did not match due to a non uppercase char, to review:\n")
        for match in no_match:
            log.write(str(match))
            log.write("\n")

    for line in norm_text:
        norm.write(f"{line}\n")