import spacy
import csv

def preprocessing(file):
    clean = []
    for line in file.read().splitlines():
        line = line.strip().replace('\t', '').replace('—', '-').replace('’', '\'')
        if line: #this will only append non empty lines
            clean.append(line)
   
    return clean

models = ["fr_core_news_sm", "fr_core_news_md", "fr_core_news_lg", "fr_dep_news_trf"]
book_name = "Arsène_Lupin_gentleman-cambrioleur"


with open(".\\books\\" + book_name + ".txt" , mode='r', encoding='utf-8') as file:
    file = preprocessing(file)
    for model in models:
        nlp = spacy.load(model)
        with open(".\\output\\" + book_name + "_" + model + ".csv", mode = 'w', encoding= 'utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['entity', 'label', 'occurence'])
            writer.writeheader()
            entities = {}

            for line in file:   
                doc = nlp(line)
                for ent in doc.ents:
                    if ent.text not in entities.keys():
                        entities[ent.text] = {"label" :ent.label_, "occurence": 1}
                    else:
                        entities[ent.text]["occurence"] = entities[ent.text]["occurence"] + 1
           
            # This sorts the dictionnary by the key "occurence" of the nested dictionary
            sorted_output = sorted(entities.items(), key=lambda x: x[1]["occurence"], reverse=True)
            # print(sorted_output)
            
            for key, value in sorted_output:
                writer.writerow({'entity': key, 'label': value['label'], 'occurence': value['occurence']})
        csvfile.close()
