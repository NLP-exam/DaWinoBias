"""Contains two functions: load_texts and load_occs
load_texts: Load DaWinoBias texts 
load_occ: Load occupations
"""

import os
from pathlib import Path

def load_texts(path,condition,dev_test):
    """load DaWinoBias texts 
    """    

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

def load_occs(female=False,male=False):
    """Load occupations

    Keyword Arguments:
        female {bool} -- [Whether to include occupations that defined as stereotypically female] (default: {False})
        male {bool} -- [Whether to include occupations that defined as stereotypically female] (default: {False})

    Returns:
        [Two lists] -- [One list with all occupations, one list with occupations excluding the possessive case]
    """    
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