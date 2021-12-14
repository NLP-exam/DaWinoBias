import os
from utility_fcs import load_texts, load_occs
from collections import Counter

def load_occ(female=False,male=False):
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
        'designeren','frisøren','forfatteren','husholdersken','bageren',
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
    return all_occupations, occupations_no_poss, occupations_poss


# load data 
path = os.path.join("nlp","Detecting-Bias-in--LMs","data")
anti_lines = load_texts(path,"anti", "both")
pro_lines = load_texts(path,"pro", "both")

# flatten lines to one list
anti_lines = [sentence for sublist in anti_lines for sentence in sublist]

# make data one string
anti_lines = ' '.join(anti_lines)
anti_lines = anti_lines.lower()

# load occupations
_, occ_no_poss, occ_poss = load_occ(female=True,male=True)
_, f_occ_no_poss, f_occ_poss = load_occ(female=True)
_, m_occ_no_poss, m_occ_poss = load_occ(male=True)

# count of each occupation is present in data 
occ_dic = {occ: anti_lines.count(occ) for occ in occ_no_poss}
occ_dic['assistenten'] = occ_dic['assistenten'] - occ_dic['kontorassistenten'] - occ_dic['rengøringsassistenten'] 

# get count/percentage of how many female vs. male stereotypical occupations
stereo_f_dic = {occ: anti_lines.count(occ) for occ in f_occ_no_poss}
stereo_m_dic = {occ: anti_lines.count(occ) for occ in m_occ_no_poss}
f_sum = sum(stereo_f_dic.values())
m_sum = sum(stereo_m_dic.values())
total = f_sum + m_sum
print(round(f_sum/total,2),round(m_sum/total,2))

# check position? 
