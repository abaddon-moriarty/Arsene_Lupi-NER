import requests
from bs4 import BeautifulSoup
import json

url = "https://fr.wikipedia.org/wiki/Liste_des_pseudonymes_utilis%C3%A9s_par_Ars%C3%A8ne_Lupin"
alias_list = []
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
soup.prettify()

# The alias are the only list items that have bold text, so within the "li" tags, I will look for "b" tags.
tags = soup.find_all("li")

for tag in tags:
    alias = tag.find_all("b") #searches for all "b" tags
    # only add it to the list if not empty, otherwise we end up with multiple empty entries
    if alias:
        for al in alias: #The alias are each ones within a list, so I need to loop through each item/alias.
            print(al)
            al = str(al.text).strip().replace(":", "") #removing some lost ":" that were included within the bold text (some were not)
            alias_list.append(al)

for alias in alias_list:
    print(alias)



with open ("./Arsene_Lupi-NER/tutorial/data/alias.json", "w", encoding="utf-8") as f:
    json.dump(alias_list, f, indent=4)


