# Arsene_Lupi-NER

Trying to create an NER specifically for location in the french books called "Arsène Lupin", and at some point overlap this with the Map of France.

# Tutorial Folder

In the tutorial folder you will find my work, following a playlist from Python Tutorials for Digital Humanities on youtube.

The Named Entity Recognition for Digital Humanities playlist seems to go over most aspects of NER, from rule based NER (taking NE from a list) to training our own model. So I will be following their videos.

Keeping in mind that this is work in progress to help me learn NERs and tools in NLP in general, so I will probably be using libraries that are outdated or scripts that are way too slow for what they do and that could be improved. The ultimate goal is of course to get it as close to perfection as I can, but yeah. work in progress.

In[ video 2](https://www.youtube.com/watch?v=O_2uq0sdCQo&list=PL2VXyKi-KpYs1bSnT8bfMFyGS-wMcjesM&index=2), they work on Harry Potter and detecting names from the books. I'll stick to People and not location for this video for educational purposes. I will however apply this directly to Arsène Lupin, even just to get to know the source material a bit better.

I haven't found a list of all Arsène Lupin characters, however there is a list of all AL aliases he uses throughout the books. The list is much shorter but the code should work the same and get me to understand NERs better.

## alias_scraper

I am using the beautiful soup code that he showed, because I've never used that library (and don't know what I'm doing). And trying to apply it to my Wiki page. I have to adapt it because his and my pages don't have the same format (despite both being lists of Wikipedia).

# Libraries Used
 
 - SpaCy
 - Beautiful Soup
