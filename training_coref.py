#Loading data 
from danlp.datasets import Dacoref
dacoref = Dacoref()
# The corpus can be loaded with or without splitting into train, dev and test in a list in that order
corpus = dacoref.load_as_conllu(predefined_splits=True)

#Importing neuralcoref
import spacy
import neuralcoref

nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)
doc1 = nlp('My sister has a dog. She loves him.')
print(doc1._.coref_clusters)

doc2 = nlp('Angela lives in Boston. She is quite happy in that city.')
for ent in doc2.ents:
    print(ent._.coref_cluster)

