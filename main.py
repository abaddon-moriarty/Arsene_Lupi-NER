import spacy
import csv
import os

from spacy.matcher import Matcher
from os.path import isfile, join
from os import listdir

# This cleans out the text from character that might cause issues, right now only "\n", "\t", "—" and "’"
# List to be updated throughout dev
def preprocessing(file):
    clean = []
    for line in file.read().splitlines():
        line = line.strip().replace('\t', '').replace('—', '-').replace('’', '\'')
        if line: #this will only append non empty lines
            clean.append(line)

    return clean


# loop to go through all files in the input dir, so we can analyse each text with one command
def bibli(path):
    all_paths = [file for file in listdir(path) if isfile(join(path,file))]
    return all_paths

models = ["fr_core_news_sm"] #, "fr_core_news_md", "fr_core_news_lg", "fr_dep_news_trf"]
book_name = "Arsène_Lupin_gentleman-cambrioleur"
path = ".\\books\\"


# This loop will list all files in the dir books. right now all_paths is hardcoded as only one book.
# To run this all comment out the lines below
# all_paths = bibli(path)
all_paths = [book_name + ".txt"]
for book_name in all_paths:
    with open(join(path + book_name) , mode='r', encoding='utf-8') as file:
        file = preprocessing(file)

        for model in models:
            nlp = spacy.load(model)
            
            with open(".\\output\\" + book_name[:-4] + "_" + model + ".csv", mode = 'w', encoding= 'utf-8', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['entity', 'label', 'occurence'])
                writer.writeheader()
                entities = {}
        
                #loops through all lines adding the entities in a dictionnary
                for line in file:   
                    doc = nlp(line)
                    for ent in doc.ents:
                        # checks if the entity is already in our dictionnary
                        if ent.text not in entities.keys():
                            entities[ent.text] = {"label" :ent.label_, "occurence": 1}
                        else:
                            if entities[ent.text]["label"] != ent.label_:
                                entities[ent.text] = {"label" :ent.label_, "occurence": 1}
                            else:
                                entities[ent.text]["occurence"] = entities[ent.text]["occurence"] + 1
            
                # This sorts the dictionnary by the key "occurence" of the nested dictionary
                sorted_output = sorted(entities.items(), key=lambda x: x[1]["occurence"], reverse=True)
                # print(sorted_output)
                
                # prints out in csv file
                for key, value in sorted_output:
                    writer.writerow({'entity': key, 'label': value['label'], 'occurence': value['occurence']})
            csvfile.close()
