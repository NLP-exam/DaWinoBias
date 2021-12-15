import sys, os, spacy, random
from pathlib import Path
import numpy as np
from danlp.models import load_xlmr_coref_model
from utility_fcs import idx_occ_pron, remove_sq_br, load_texts, load_occs
from model_evaluation import evaluate_model

# load the coreference model
coref_model = load_xlmr_coref_model()

#load model used for tokenization
nlp = spacy.load("da_core_news_lg") 

#load doc
path = os.path.join("data")
anti_lines = load_texts(path,"anti", "both")
pro_lines = load_texts(path,"pro", "both")

# flatten lists
anti_lines = [sentence for sublist in anti_lines for sentence in sublist]
pro_lines = [sentence for sublist in pro_lines for sentence in sublist]

# randomize data 
random.shuffle(anti_lines)
random.shuffle(pro_lines)

#define occupations
occupations_male, _ = load_occs(male=True)
occupations_female, _ = load_occs(female=True)

for condition in ['anti_stereotypical', 'pro_stereotypical']:
    if condition == 'anti_stereotypical':
        lines = anti_lines
    elif condition == 'pro_stereotypical':
        lines = pro_lines

    # prediction results: [successful preds, unsuccessful preds, failed preds]
    pred_res = [0,0,0]
    labels, preds = [], []
    labels_occ, preds_occ = [], []
    labels_steretypical, preds_steretypical = [], []

    # Look through sentences
    for line in lines: 
        # convert to nlp object
        line = nlp(line)

        # tokenize and lowercase
        tokens = []
        for token in line:
            tokens.append(token.text.lower())
        
        # get correct coref and incorrect coref to compare with predictions
        coref_res,_ = idx_occ_pron(tokens)
        
        # remove square brackets 
        tokens = remove_sq_br(tokens)
        
        # apply coreference resolution to the document and get a list of clusters
        clusters = coref_model.predict_clusters(tokens)

        # get token indices from predicted cluster
        if len(clusters) == 0:
            cluster_idx = [-1]
        else:
            cluster_idx = [i[1] for i in clusters[0]]
        
        # compare predicted clusters with correct res
        if cluster_idx == coref_res[0]:
            pred_res[0] += 1
        elif cluster_idx == coref_res[1]:
            pred_res[1] += 1
        else: 
            pred_res[2] += 1

        # labels 
        labels.append(coref_res[0][0])
        
        #predictions
        if len(cluster_idx)>2 or len(cluster_idx)<1: 
            preds.append(-1)
        elif len(cluster_idx)==2:
            preds.append(cluster_idx[0])
        
        #occupation labels
        labels_occ.append(tokens[0][coref_res[0][0]])
        preds_occ.append(tokens[0][cluster_idx[0]])

    
    

    #get results in table
    evaluate_model(labels_occ, preds_occ, filename = f'results/{condition}_results_occupations')

    #print results
    print(evaluate_model(labels_occ, preds_occ, filename = f'results/{condition}_results_occupations'))

