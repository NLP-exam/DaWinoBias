import spacy
from danlp.models import load_xlmr_coref_model
import sys, os
from pathlib import Path
import numpy as np
from utility_fcs import idx_occ_pron, remove_sq_br

# load the coreference model
coref_model = load_xlmr_coref_model()

# a document is a list of tokenized sentences
doc = [["Lotte", "arbejder", "med", "Mads", "Emil","."], ["Hun", "er", "tandlæge", "."], ["Han", "er", "assistent"]]

example = '[Udvikleren] diskuterede med designeren, fordi [hun] ikke kunne lide designet.'
example2 = 'Udvikleren diskuterede med [designeren], fordi [hans] idé ikke kan blive implementeret.'
example3 = 'Mekanikeren gav [kontorassistenten] en gave, fordi det var [hans] fødselsdag.'

#load doc
path= os.path.join("NLP","Detecting-Bias-in--LMs","data")

for filepath in Path(path).glob("*.txt"):
    with open(filepath) as file:
        text = file.readlines()
        lines = [line.rstrip() for line in text]

#print example sentences
print(lines)

results = []
#tokenise
for line in lines: 
    #load model
    nlp = spacy.load("da_core_news_lg")

    #convert to nlp object
    doc = nlp(line)

    #tokenize and lowercase
    tokens = []
    for token in doc:
        tokens.append(token.text.lower())

    print(tokens)

    coref_res = idx_occ_pron(tokens)
    print(coref_res)
    tokens = remove_sq_br(tokens)


    # apply coreference resolution to the document and get a list of features (see below)
    preds = coref_model.predict(tokens)

    # apply coreference resolution to the document and get a list of clusters
    clusters = coref_model.predict_clusters(tokens)

    results.append(clusters)
    print(clusters)