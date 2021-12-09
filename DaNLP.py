import sys, os, spacy
from pathlib import Path
import numpy as np
from danlp.models import load_xlmr_coref_model
from utility_fcs import idx_occ_pron, remove_sq_br, load_texts, get_pred_res

# load the coreference model
coref_model = load_xlmr_coref_model()

#load model used for tokenization
nlp = spacy.load("da_core_news_lg") 

#load doc
path = os.path.join("nlp","Detecting-Bias-in--LMs","data")
anti_lines = load_texts(path,"anti")
pro_lines = load_texts(path,"pro")

# flatten lists
anti_lines = [sentence for sublist in anti_lines for sentence in sublist]
pro_lines = [sentence for sublist in pro_lines for sentence in sublist]

# get count on preds
anti_pred_res = get_pred_res(anti_lines, coref_model, nlp)
pro_pred_res = get_pred_res(pro_lines, coref_model, nlp)

# print results
print("anti_pred:" ,anti_pred_res)
print("pro_pred:" ,pro_pred_res)