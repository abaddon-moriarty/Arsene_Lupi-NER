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
# def bibli(path):
#     all_paths = [file for file in listdir(path) if isfile(join(path,file))]
#     return all_paths

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

                """The dict should look like this:
                entities = {Herlock Sholmès:{
                                            'PER': 32,
                                            'LOC': 4,}
        
                """

                #loops through all lines adding the entities in a dictionnary
                for line in file:   
                    doc = nlp(line)
                    for ent in doc.ents:
                        # checks if the entity is already in our dictionnary
                        if ent.text not in entities.keys():
                            entities[ent.text] = {ent.label_: 1}
                            entities[ent.text]["total"] = 1
                        else:
                            #checks if the label linked to the entity is the same if it is just add 1 occurence, 
                            # if not adds a new key, value pair.
                            # also counting total number of occurence so it's easier to sort out later.
                            if ent.label_ not in entities[ent.text].keys():
                                entities[ent.text][ent.label_] = 1
                                entities[ent.text]["total"] += 1             
                            else:
                                entities[ent.text][ent.label_] = entities[ent.text][ent.label_] + 1
                                entities[ent.text]["total"] += 1
                                
                

                
                # This sorts the dictionnary by the number of total occurence across all labels, key: "total"
                sorted_output = sorted(entities.items(), key=lambda x: x[1]["total"], reverse=True)
                # prints out in csv file
                for key, value in sorted_output:
                    # write one row for the total amount of occurences
                    writer.writerow({'entity': key, 
                                    'label': "total", 
                                    'occurence': value["total"]})

                    #write one row per label attributed to the entity // one row per item in the dict
                    for k, val in value.items():
                        if k != 'total':

                            # label = [k for k in value.keys() if k != "total"]
                            # occurence = [(k, val) for k, val in value.items() if k != "total"]
                            writer.writerow({'entity': key, 
                                            'label': k, 
                                            'occurence': val})


            csvfile.close()