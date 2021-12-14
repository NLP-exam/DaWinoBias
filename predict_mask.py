from utility_fcs import idx_occ_pron, remove_sq_br, load_texts, get_pred_res

def predict_masked(lines, nlp, tokenizer): 
    #initialize predictions and labels 
    labels, preds = [], []

    for line in lines:
        #convert to nlp object
        line = tokenizer(line)

        #tokenize and lowercase
        tokens = []
        for token in line:
            tokens.append(token.text.lower())
        
        #find index of pronoun
        _, prons_idx = idx_occ_pron(tokens)

        #remove square brackets
        tokens = remove_sq_br(tokens)[0]

        #save correct pronoun
        correct_pronoun = tokens[prons_idx]

        #MASK pronouns
        tokens[prons_idx] = '[MASK]'

        #collected sentence
        sentence = ' '.join(tokens)
        
        #save prediction
        pred = nlp(sentence)[0]['token_str']

        #labels and predictions
        labels.append(correct_pronoun)
        preds.append(pred)
    return labels, preds

