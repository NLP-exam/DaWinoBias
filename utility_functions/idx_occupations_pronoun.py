import os
from pathlib import Path
from utility_functions.load_data import load_occs
from utility_functions.remove_square_brackets import remove_sq_br

def idx_occ_pron(tokens):
    """Get indicies of correct cluster and incorrect cluster as well as pronoun index. 
    Correct cluster: Indicies of pronoun and the occupation is refers to. 
    Incorrect cluster: Indicides of pronoun and the occupation is *does not* refer to.  

    Only used for DaNLP coref model
    """    
    #define occupations
    occupations, _ = load_occs(female = True, male=True)

    #define pronouns
    pronouns = ['hans', 'hendes', 'han', 'hun', 'ham', 'hende']

    #define square brackets
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

def get_pred_res():
    pass
