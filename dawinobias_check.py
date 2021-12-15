import os, spacy
from collections import Counter
import random 

from utility_functions.load_data import load_texts, load_occs
from utility_functions.remove_square_brackets import remove_sq_br

#load model used for tokenization
nlp = spacy.load("da_core_news_lg") 

# load data - we just use anti for this, since pro and anti are identical (except for pronouns)
path = os.path.join("data")
anti_lines = load_texts(path,"anti", "both")

# flatten data to one list
anti_lines = [sentence for sublist in anti_lines for sentence in sublist]

# make data one string
anti_lines_str = ' '.join(anti_lines)
anti_lines_str = anti_lines_str.lower()

# load occupations
all_occ, occ_no_poss = load_occs(female=True,male=True)
_, f_occ_no_poss = load_occs(female=True)
_, m_occ_no_poss = load_occs(male=True)

# count of each occupation is present in data 
occ_dic = {occ: anti_lines_str.count(occ) for occ in occ_no_poss}
occ_dic['assistenten'] = occ_dic['assistenten'] - occ_dic['kontorassistenten'] - occ_dic['rengøringsassistenten'] 

# get percentage of how many female vs. male stereotypical occupations
stereo_f_dic = {occ: anti_lines_str.count(occ) for occ in f_occ_no_poss}
stereo_m_dic = {occ: anti_lines_str.count(occ) for occ in m_occ_no_poss}
f_sum = sum(stereo_f_dic.values())
m_sum = sum(stereo_m_dic.values())
total = f_sum + m_sum

print("% female and male stereotypical occupations in DaWinoBias")
print(round(f_sum/total,2),round(m_sum/total,2))

# Position check
pos_0=''
for line in anti_lines:
    # make line nlp object
    line = nlp(line)

    # tokenize and lowercase
    tokens = []
    for token in line:
        tokens.append(token.text.lower())

    #remove [ and ]
    tokens = remove_sq_br(tokens)[0]

    # get 
    pos_0 += tokens[0] + ' '


stereo_f_dic = {occ: pos_0.count(occ) for occ in f_occ_no_poss}
stereo_m_dic = {occ: pos_0.count(occ) for occ in m_occ_no_poss}
f_sum = sum(stereo_f_dic.values())
m_sum = sum(stereo_m_dic.values())
total = f_sum + m_sum

print("% stereotypical female and male occupations that are the first element in the sentences")
print(round(f_sum/total,2),round(m_sum/total,2))