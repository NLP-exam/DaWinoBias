import sys, os, spacy
from pathlib import Path
import numpy as np
from danlp.models import load_xlmr_coref_model
from utility_fcs import idx_occ_pron, remove_sq_br, load_texts, get_pred_res
from model_evaluation import evaluate_model

# load the coreference model
coref_model = load_xlmr_coref_model()

#load model used for tokenization
nlp = spacy.load("da_core_news_lg") 

#load doc
path = os.path.join("NLP","Detecting-Bias-in--LMs","data")
anti_lines = load_texts(path,"anti", "both")
pro_lines = load_texts(path,"pro", "both")

# flatten lists
anti_lines = [sentence for sublist in anti_lines for sentence in sublist]
pro_lines = [sentence for sublist in pro_lines for sentence in sublist]

# get count on preds
anti_pred_res, anti_labels, anti_preds  = get_pred_res(anti_lines, coref_model, nlp)
pro_pred_res, pro_labels, pro_preds = get_pred_res(pro_lines, coref_model, nlp)
print('anti_labels',anti_labels)
print('anti_preds',anti_preds)
'''
print('anti_pred_res', anti_pred_res)
print('anti_labels',anti_labels)
print('anti_preds', anti_preds)
'''
#get results in table
print(evaluate_model(anti_labels, anti_preds, filename = 'anti_results'))
print(evaluate_model(pro_labels, pro_preds, filename = 'pro_results'))

# print results
print("anti_pred:" ,anti_pred_res)
print("pro_pred:" ,pro_pred_res)
