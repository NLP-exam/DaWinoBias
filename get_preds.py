from utility_fcs import idx_occ_pron, remove_sq_br

def get_pred_res(lines,coref_model, nlp): 
    occupations_male = ['chaufføren', 'supervisoren', 'viceværten', 'kokken', 'flyttemanden', 
    'entreprenøren', 'lederen', 'udvikleren', 'tømreren', 'bestyreren', 
    'advokaten', 'landmanden', 'sælgeren', 'lægen', 'vagten', 
    'analytikeren', 'mekanikeren', 'direktøren','bygningsarbejderen']
    occupations_male_poss = [occ + 's' for occ in occupations_male] # possessive case

    occupations_female = ['kassedamen', 'læreren','sygeplejersken','assistenten','sekretæren',
    'revisoren','rengøringsassistenten','receptionisten','kontorassistenten','rådgiveren',
    'designeren','frisøren','forfatteren','husholdersken','bageren',
    'bogholderen','redaktøren','bibliotekaren','syersken']
    occupations_female_poss = [occ + 's' for occ in occupations_female] # possessive case

    #create one coherent occupations list
    occupations = []
    occupations.append(occupations_male)
    occupations.append(occupations_male_poss)
    occupations.append(occupations_female)
    occupations.append(occupations_female_poss)

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
        
        # apply coreference resolution model to the sentence and get a list of clusters
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

        #stereotypical labels
        if tokens[0][labels[-1]] in occupations_female and preds[-1] != -1: 
            labels_steretypical.append('stereotypical_female')
        if tokens[0][labels[-1]] in occupations_male and preds[-1] != -1: 
            labels_steretypical.append('stereotypical_male')

        #stereotypical predictions
        if tokens[0][preds[-1]] in occupations_female and preds[-1] != -1: 
            preds_steretypical.append('stereotypical_female')
        if tokens[0][preds[-1]] in occupations_male and preds[-1] != -1: 
            preds_steretypical.append('stereotypical_male')
    
    # get pred_res in percentages 
    total_sentences = sum(pred_res)
    pred_res[0] = round(pred_res[0]/total_sentences,2)
    pred_res[1] = round(pred_res[1]/total_sentences,2)
    pred_res[2] = round(pred_res[2]/total_sentences,2)
    return pred_res, labels_occ, preds_occ