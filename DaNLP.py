from danlp.models import load_xlmr_coref_model
import sys, os
from pathlib import Path
from 

# load the coreference model
coref_model = load_xlmr_coref_model()

# a document is a list of tokenized sentences
doc = [["Lotte", "arbejder", "med", "Mads", "Emil","."], ["Hun", "er", "tandlæge", "."], ["Han", "er", "assistent"]]

#load doc
path = os.path.join("NLP","Detecting-Bias-in--LMs","data")

for filepath in Path(path).glob("*.txt"):
    with open(filepath) as file:
        text = file.readlines()
        text = [[sentence.rstrip()] for sentence in text]

#tokenise


# apply coreference resolution to the document and get a list of features (see below)
preds = coref_model.predict(doc)

# apply coreference resolution to the document and get a list of clusters
clusters = coref_model.predict_clusters(doc)

print(preds)

print(clusters)