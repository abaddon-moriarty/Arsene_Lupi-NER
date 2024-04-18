import os

modifs = []
punkt = "!\"#$%&'’()*+,./:;<=>?@[\\]^_`{|}~«»… ⁂"

root = "C:\\Users\\munau\\OneDrive\\Desktop\\Machine_Learning\\Arsène Lupin Project\\Arsene_Lupi-NER\\"
book_dir = f"{root}books\\"

x = 1
while os.path.exists(f"C:\\Users\\munau\\OneDrive\\Desktop\\Machine_Learning\\Arsène Lupin Project\\Arsene_Lupi-NER\\log\\preprocessing_{x}.log"):
    x = x + 1

for bookname in os.listdir(book_dir):

    norm_name = f"{root}input\\{bookname[:-4]}_norm{bookname[-4:]}"
    log = open(f"{root}log\\preprocessing_{x}.log", "a", encoding='utf-8')
    f = open(os.path.join(book_dir, bookname), "r", encoding='utf-8')
    norm = open(f"{root}input\\{bookname[:-4]}_norm{bookname[-4:]}", "w", encoding='utf-8')


    log.write(f"Pre-processing the book: {bookname}.\n")
    print(f"Pre-processing the book: {bookname}.\n")
    book = f.read().split("\n\n")
    segments = []
    no_match = []
    norm_text = []
    mods = 0
    for segment in book:
        segment = segment.strip()
        if segment: #removing empty items
            segments.append(segment.strip())
    for i, segment in enumerate(segments):
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
        # norm_text.append(segments)
        norm.write(f"{segments[i]}\n")
        # norm.write(f"{segments[i]}\n")
        # norm.write("\n")
            
    print(f"in the book: \"{bookname}\", {mods} lines were modified.\n")
    log.write(f"Total of {mods} line merges were made.\nThe following lines did not match due to a non uppercase char, to review:\n")
    for match in no_match:
        log.write(str(match))
        log.write("\n")

    for line in norm_text:
        norm.write(f"{line}\n")