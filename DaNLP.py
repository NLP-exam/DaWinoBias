from danlp.models import load_xlmr_coref_model

# load the coreference model
coref_model = load_xlmr_coref_model()

# a document is a list of tokenized sentences
doc = [["Lotte", "arbejder", "med", "Mads", "."], ["Hun", "er", "tandlæge", "."]]

# apply coreference resolution to the document and get a list of features (see below)
preds = coref_model.predict(doc)

# apply coreference resolution to the document and get a list of clusters
clusters = coref_model.predict_clusters(doc)