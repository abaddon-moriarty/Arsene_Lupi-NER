import csv
import time
from os import listdir
from os.path import isfile, join

import spacy
from spacy.matcher import Matcher
from tqdm import tqdm

total_start_time = time.time()


# This cleans out the text from character that might cause issues, right now only "\n", "\t", "—" and "’"
# List to be updated throughout dev
def preprocessing(file):
    clean = []
    f = file.read().splitlines()
    for line in tqdm(f, desc="cleaning the text", unit=" line"):
        # for line in f:
        line = line.strip().replace("\t", "").replace("—", "-").replace("’", "'")
        if line:  # this will only append non empty lines
            clean.append(line)

    return clean


# loop to go through all files in the input dir, so we can analyse each text with one command
def bibli(path):
    all_paths = [file for file in listdir(path) if isfile(join(path, file))]
    return all_paths


def loading_models(models):
    # Pre-loading models so it's accessible for processing
    for model in models.keys():
        print(f"loading the model: {model}")
        start_time = time.time()
        models[model]["nlp"] = spacy.load(model)
        models[model]["matcher"] = Matcher(models[model]["nlp"].vocab)
        end_time = time.time()
        print(f"Time to load the model: {model}", end_time - start_time)
    return models


models = {
    "fr_core_news_sm": {"nlp": None, "matcher": None},
    "fr_core_news_md": {"nlp": None, "matcher": None},
    "fr_core_news_lg": {"nlp": None, "matcher": None},
    # "fr_dep_news_trf": {"nlp": None, "matcher": None},
}

models = loading_models(models)
book_name = "Arsène_Lupin_gentleman-cambrioleur_norm"
path = "./input/"


# This loop will list all files in the dir books. right now all_paths is hardcoded as only one book.
# To run this all comment out the lines below
# all_paths = bibli(path)
all_paths = [book_name + ".txt"]

for book_name in tqdm(all_paths, unit=" book"):
    with open(join(path + book_name), mode="r", encoding="utf-8") as file:
        with open("LOC_sm.txt", mode="w", encoding="utf-8") as text:
            file = preprocessing(file)
            print("working on:", book_name)
            for model in models.keys():
                print("Using the model", model)
                start_time = time.time()
                nlp = models[model]["nlp"]
                matcher = models[model]["matcher"]
                end_time = time.time()
                print(f"Time to load the model: {model}", end_time - start_time)

                for f in tqdm(file):
                    doc = nlp(f)

                    # The pattern is tring to match any Entity type Location, that does not look like an url or an e-mail because I've had a few of those in first runs.
                    pattern = [
                        {"ENT_TYPE": "LOC"},
                        {"LIKE_NUM": False},
                        {"LIKE_URL": False},
                        {"LIKE_EMAIL": False},
                    ]
                    matcher.add("LOC_PATTERN", [pattern])
                    matches = matcher(doc)

                    # print(len(matcher), "correspondances found.")
                    for match_id, start, end in matches:
                        deps = []
                        # Obtiens le span en correspondance
                        matched_span = doc[start:end]
                        # print(matched_span.text)
                        text.write(matched_span.text)
                        for token in matched_span:
                            deps.append(token.dep_)
                        text.write(str(deps))
                        text.write("\n")

                        # matched_dep = matched_span.dep_
                        # text.write("\n")

                with open(
                    "./output/" + book_name[:-4] + "_" + model + ".csv",
                    mode="w",
                    encoding="utf-8",
                    newline="",
                ) as csvfile:
                    writer = csv.DictWriter(
                        csvfile, fieldnames=["entity", "label", "occurence"]
                    )
                    writer.writeheader()
                    entities = {}
                    """The dict should look like this:
                    entities = {Herlock Sholmès:{
                                                'PER': 32,
                                                'LOC': 4,}
                    """

                    # loops through all lines adding the entities in a dictionnary
                    for line in tqdm(file, unit=" line"):
                        doc = nlp(line)

                        for ent in doc.ents:
                            if ent.label_ == "LOC":
                                # checks if the entity is already in our dictionnary
                                if ent.text not in entities.keys():
                                    entities[ent.text] = {ent.label_: 1}
                                    entities[ent.text]["total"] = 1
                                else:
                                    # checks if the label linked to the entity is the same if it is just add 1 occurence,
                                    # if not adds a new key, value pair.
                                    # also counting total number of occurence so it's easier to sort out later.
                                    if ent.label_ not in entities[ent.text].keys():
                                        entities[ent.text][ent.label_] = 1
                                        entities[ent.text]["total"] += 1
                                    else:
                                        entities[ent.text][ent.label_] = (
                                            entities[ent.text][ent.label_] + 1
                                        )
                                        entities[ent.text]["total"] += 1

                    # This sorts the dictionnary by the number of total occurence across all labels, key: "total"
                    sorted_output = sorted(
                        entities.items(), key=lambda x: x[1]["total"], reverse=True
                    )
                    # prints out in csv file
                    for key, value in sorted_output:
                        # write one row for the total amount of occurences
                        writer.writerow(
                            {
                                "entity": key,
                                "label": "total",
                                "occurence": value["total"],
                            }
                        )

                        # write one row per label attributed to the entity // one row per item in the dict
                        for k, val in value.items():
                            if k != "total":
                                # label = [k for k in value.keys() if k != "total"]
                                # occurence = [(k, val) for k, val in value.items() if k != "total"]
                                writer.writerow(
                                    {"entity": key, "label": k, "occurence": val}
                                )

                    csvfile.close()

                    print(
                        "\nThe model",
                        model,
                        "found",
                        len(sorted_output),
                        "different entities",
                    )

total_end_time = time.time()

print(f"Total run time: {total_end_time - total_start_time}")
