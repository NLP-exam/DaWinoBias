import os
from pathlib import Path

def get_pred_res():
    pass

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

def remove_sq_br(tokens):
    #input tokens to remove '[]' 
    return [[token for token in tokens if token != '[' and token != ']']]


def load_occs(female=False,male=False):
    all_occupations, occupations_no_poss, occupations_poss = [], [], []
    if male:
        occupations_male = ['chaufføren', 'supervisoren', 'viceværten', 'kokken', 'flyttemanden', 
        'bygningsarbejderen', 'lederen', 'udvikleren', 'tømreren', 'bestyreren', 
        'advokaten', 'landmanden', 'sælgeren', 'lægen', 'vagten', 
        'analytikeren', 'mekanikeren', 'direktøren']
        occupations_male_poss = [occ + 's' for occ in occupations_male] # possessive case

    if female:
        occupations_female = ['ekspedienten', 'læreren','sygeplejersken','assistenten','sekretæren',
        'revisoren','rengøringsassistenten','receptionisten','kontorassistenten','rådgiveren',
        'designeren','frisøren','skribenten','husholdersken','bageren',
        'bogholderen','redaktøren','bibliotekaren','syersken']
        occupations_female_poss = [occ + 's' for occ in occupations_female] # possessive case

    if male and not female: 
        # occ's without pos and with pos
        occupations_no_poss, occupations_poss = occupations_male, occupations_male_poss

    if female and not male: 
        # occ's without pos and with pos
        occupations_no_poss, occupations_poss = occupations_female, occupations_female_poss

    if male and female:
        # list with occ's without possessive case
        occupations_no_poss = occupations_male + occupations_female
        # list with occ's with possessive case
        occupations_poss = occupations_male_poss + occupations_female_poss

    # list with all occupations
    all_occupations = occupations_no_poss + occupations_poss

    return all_occupations, occupations_no_poss
