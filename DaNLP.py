import spacy
from danlp.models import load_xlmr_coref_model
import sys, os
from pathlib import Path

# load the coreference model
coref_model = load_xlmr_coref_model()

# a document is a list of tokenized sentences
doc = [["Lotte", "arbejder", "med", "Mads", "Emil","."], ["Hun", "er", "tandlæge", "."], ["Han", "er", "assistent"]]

#save indices of coreferenced tokens, i.e. []
occupations = ['Chaufføren', 'Supervisoren', 'Viceværten', 'Kokken', 'Flyttemanden', 
'Den ufaglærte', 'Entreprenøren', 'Lederen', 'Udvikleren', 'Tømreren', 'Manageren', 'Advokaten', 
'Landmanden', 'Sælgeren', 'Lægen', 'Vagten', 'Analytikeren', 'Mekanikeren', 'CEOen','Kassedamen',
'Læreren','Sygeplejerske','Assistent','Sekretæren','Revisoren','Rengøringsassistenten','Receptionisten'
,'Kontorassistenten','Rådgiveren','Designeren','Frisøren','Forfatteren','Husholdersken','Bageren','Bogholderen'
,'Redaktøren','Bibliotekaren','Syersken']

#load doc
path= os.path.join("NLP","Detecting-Bias-in--LMs","data")

for filepath in Path(path).glob("*.txt"):
    with open(filepath) as file:
        text = file.readlines()
        lines = [line.rstrip() for line in text]

#print example sentences
print(lines[0])

#tokenise
nlp = spacy.load("da_core_news_lg")
doc = nlp(lines[0])
print(doc.text)

tokens = []
for token in doc:
    tokens.append(token.text)

print(tokens)

#Kiris kode
#print(tokens)
#print([i for i in occupations if i in tokens])
#tokens.index([i for i in occupations if i in tokens][0])

#get indices of coreferenced pairs
coref_pair_idx = []
for idx, token in enumerate(tokens):
    if idx < 1 and token == '[':
        coref_pair_idx.append(idx)
    elif idx > 1 and token == '[':
        coref_pair_idx.append(idx-2)

# apply coreference resolution to the document and get a list of features (see below)
#preds = coref_model.predict(doc)

# apply coreference resolution to the document and get a list of clusters
#clusters = coref_model.predict_clusters(doc)

#print(preds)

#print(clusters)