import csv
import time
from os import listdir
from os.path import isfile, join, splitext

import spacy
from spacy.matcher import Matcher
from tqdm import tqdm

total_start_time = time.time()


# loop to go through all files in the input dir, so we can analyse each text with one command
def get_all_files(path):
    """
    Retrieve all files in a given directory.

    Args:
        path (str): The directory path to search for files.

    Returns:
        list: A list of filenames (strings) in the specified directory.

    Example:
        >>> get_all_files('/home/user/documents')
        ['file1.txt', 'file2.pdf', 'file3.py']
    """
    return [file for file in listdir(path) if isfile(join(path, file))]


def loading_models(models):
    """
    Load and initialize spaCy NLP models with matchers.
    This function pre-loads spaCy models and creates Matcher objects for each model,
    making them accessible for subsequent NER processing. It measures and prints the
    loading time for each model.
    Args:
        models (dict): A dictionary where keys are model names (str) and values are
                       dictionaries that will be updated with 'nlp' and 'matcher' keys.
    Returns:
        dict: The input models dictionary updated with 'nlp' (spaCy Language object)
              and 'matcher' (Matcher object) for each model.
    Raises:
        OSError: If a spaCy model cannot be found or loaded.
    Example:
        >>> models = {'en_core_web_sm': {}, 'en_core_web_md': {}}
        >>> loaded_models = loading_models(models)
    """
    # Pre-loading models so it's accessible for processing
    for model in models:
        print(f"Loading the model: {model}")
        start_time = time.time()
        models[model]["nlp"] = spacy.load(model)
        models[model]["matcher"] = Matcher(models[model]["nlp"].vocab)
        end_time = time.time()
        print(f"Time to load {model}: {end_time - start_time:.2f}s")
    return models


def main():
    models = {
        "fr_core_news_sm": {"nlp": None, "matcher": None},
        "fr_core_news_md": {"nlp": None, "matcher": None},
        "fr_core_news_lg": {"nlp": None, "matcher": None},
        # "fr_dep_news_trf": {"nlp": None, "matcher": None},
    }

    models = loading_models(models)
    # book_name = "Arsène_Lupin_gentleman-cambrioleur_norm"
    path = "./input/"

    loc_pattern = [
        {"ENT_TYPE": "LOC"},
        {"LIKE_NUM": False},
        {"LIKE_URL": False},
        {"LIKE_EMAIL": False},
    ]

    # This loop will list all files in the dir books. right now all_paths is hardcoded as only one book.
    # To run this all comment out the lines below
    all_paths = get_all_files(path)
    # all_paths = [book_name + ".txt"]

    for model in models:
        print(f"\nUsing the model: {model}")
        start_time = time.time()
        nlp = models[model]["nlp"]
        matcher = models[model]["matcher"]
        end_time = time.time()
        print(f"Time to retrieve the model: {model}, {end_time - start_time:.2f}")

        # The pattern is tring to match any Entity type Location, that does not look like an url or an e-mail because I've had a few of those in first runs.
        # Moved outside of all loops, because why would you need to reinitialise it everytime ?
        # That wasn't very DRY of my, my bad.
        if "LOC_PATTERN" not in matcher:
            matcher.add("LOC_PATTERN", [loc_pattern])

        for book_name in tqdm(all_paths, desc="Processing books", unit="book"):
            # reading the file
            with open(join(path, book_name), mode="r", encoding="utf-8") as book:
                lines = book.read().splitlines()
            print(f"Working on: {book_name}")
            entities = {}
            # The dict should look like this:
            # entities = {Herlock Sholmès:{
            #                             'PER': 32,
            #                             'LOC': 4,}
            result = []

            for line in tqdm(lines, desc="Processing lines", unit="line", leave=False):
                doc = nlp(line)

                matches = matcher(doc)

                # print(len(matcher), "correspondances found.")
                for match_id, start, end in matches:
                    matched_span = doc[start:end]

                    # Obtiens le span en correspondance
                    deps = [token.dep_ for token in matched_span]
                    # print(matched_span.text)

                    result.append(f"{matched_span.text}\t{deps}\n")

                    # matched_dep = matched_span.dep_
                    # text.write("\n")

                for ent in doc.ents:
                    if ent.label_ == "LOC":
                        # checks if the entity is already in our dictionnary
                        if ent.text not in entities:
                            entities[ent.text] = {ent.label_: 1, "total": 1}
                        else:
                            # checks if the label linked to the entity is the same if it is just add 1 occurence,
                            # if not adds a new key, value pair.
                            # also counting total number of occurence so it's easier to sort out later.
                            if ent.label_ not in entities[ent.text]:
                                entities[ent.text][ent.label_] = 1
                                entities[ent.text]["total"] += 1
                            else:
                                entities[ent.text][ent.label_] += 1
                                entities[ent.text]["total"] += 1

            if result:
                match_filename = (
                    f"./output/{splitext(book_name)[0]}_{model}_matches.txt"
                )
                with open(match_filename, "w", encoding="utf-8") as mf:
                    mf.writelines(result)

            csv_filename = f"./output/{splitext(book_name)[0]}_{model}.csv"
            with open(csv_filename, "w", encoding="utf-8", newline="") as csvfile:
                writer = csv.DictWriter(
                    csvfile, fieldnames=["entity", "label", "occurrence"]
                )
                writer.writeheader()

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
                            "occurrence": value["total"],
                        }
                    )

                    # write one row per label attributed to the entity // one row per item in the dict
                    for k, val in value.items():
                        if k != "total":
                            # label = [k for k in value.keys() if k != "total"]
                            # occurence = [(k, val) for k, val in value.items() if k != "total"]
                            writer.writerow(
                                {"entity": key, "label": k, "occurrence": val}
                            )
                print(
                    f"\nThe model {model} found {len(sorted_output)} different entities"
                )

    overall_end_time = time.time()

    print(f"\nTotal run time: {overall_end_time - total_start_time:.2f}s")


if __name__ == "__main__":
    main()
