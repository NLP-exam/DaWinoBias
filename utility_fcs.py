import os
from pathlib import Path

def load_texts(path,condition,dev_test):
    lines = []
    if condition == 'anti': 
        file_condition = 'da_anti_'
    elif condition == 'pro': 
        file_condition = 'da_pro_'
    if dev_test == 'dev':
        file_set = '*_dev.txt'
    elif dev_test == 'test':
        file_set = '*_test.txt'
    elif dev_test == 'both': 
        file_set  = '*.txt'
    files = file_condition + file_set
    for filepath in Path(path).glob(files):
        with open(filepath) as file:
            text = file.readlines()
            lines.append([line.rstrip() for line in text])
    return lines

def idx_occ_pron(tokens):
    #define occupations, pronouns and '[]'
    occupations = ['chaufføren', 'supervisoren', 'viceværten', 'kokken', 'flyttemanden', 
    'ufaglærte', 'entreprenøren', 'lederen', 'udvikleren', 'tømreren', 'manageren', 'advokaten', 
    'landmanden', 'sælgeren', 'lægen', 'vagten', 'analytikeren', 'mekanikeren', 'ceoen','kassedamen',
    'læreren','sygeplejersken','assistenten','sekretæren','revisoren','rengøringsassistenten','receptionisten'
    ,'kontorassistenten','rådgiveren','designeren','frisøren','forfatteren','husholdersken','bageren','bogholderen'
    ,'redaktøren','bibliotekaren','syersken']
    pronouns = ['hans', 'hendes', 'han', 'hun']
    square_brackets = ['[']

    #empty lists
    occ_idx, sq_idx, prons_idx = [], [], []

    #find idx of pronouns 
    prons_idx = [[tokens.index(i) for i in pronouns if i in tokens][0] -3][0]

    #find correct referenced occupation in string
    sq_idx = [tokens.index(i) for i in square_brackets if i in tokens][0]

    #remove square brackets
    tokens = remove_sq_br(tokens)[0]
    
    #Find idx of occupations
    occ_idx = [tokens.index(token) for token in tokens if token in occupations]
    
    #find the incorrect referenced occupations in string
    occ_idx.remove(sq_idx)

    #save correct and incorrect answer
    correct_cluster = [sq_idx, prons_idx]
    incorrect_cluster = [occ_idx[0], prons_idx]
    return [correct_cluster, incorrect_cluster], prons_idx

def remove_sq_br(tokens):
    #remove '[]'
    return [[token for token in tokens if token != '[' and token != ']']]

def get_pred_res(lines,coref_model, nlp): 
    # prediction results: [successful preds, unsuccessful preds, failed preds]
    pred_res = [0,0,0]

    labels, preds = [], []
    labels_occ, preds_occ = [], []

    # Look through sentences
    for line in lines: 
        #convert to nlp object
        line = nlp(line)

        #tokenize and lowercase
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
        if len(cluster_idx)>2: 
            preds.append(-1)
        elif len(cluster_idx)==2:
            preds.append(cluster_idx[0])
        
        #occupation labels
        labels_occ.append(tokens[0][coref_res[0][0]])
        preds_occ.append(tokens[0][cluster_idx[0]])

    return pred_res, labels_occ, preds_occ
