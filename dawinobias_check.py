import os, spacy
from collections import Counter
import random 

from utility_functions.load_data import load_texts, load_occs
from utility_functions.remove_square_brackets import remove_sq_br
from utility_functions.idx_occupations_pronoun import idx_occ_pron

#load model used for tokenization
nlp = spacy.load("da_core_news_lg") 

# load data 
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
print("Count of each occupation:")
print(occ_dic)
print(" ")

# get percentage of how many female vs. male stereotypical occupations
stereo_f_dic = {occ: anti_lines_str.count(occ) for occ in f_occ_no_poss}
stereo_m_dic = {occ: anti_lines_str.count(occ) for occ in m_occ_no_poss}
f_sum = sum(stereo_f_dic.values())
m_sum = sum(stereo_m_dic.values())
total = f_sum + m_sum

print("Percentage female and male stereotypical occupations in DaWinoBias")
print('female stereotypical: ',round(f_sum/total,3),', male stereotypical: ',round(m_sum/total,3))
print(" ")

# Position check: How many times do female and male stereotypical occupations 
# occur as the subject (position 0) of the sentences? 

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

print("Percentage stereotypical female and male occupations that are the first element in the sentences")
print('female stereotypical: ',round(f_sum/total,3),', male stereotypical: ',round(m_sum/total,3))
print(" ")

# Test whether all occupations are in the correct coreference pair approximately 
# the same number of times
occs_correct_coref = []
for line in anti_lines:
    # make line nlp object
    line = nlp(line)

    # tokenize and lowercase
    tokens = []
    for token in line:
        tokens.append(token.text.lower())

    correct_coref_idx = idx_occ_pron(tokens)[0][0]

    correct_occ_idx = correct_coref_idx[0]

    #remove [ and ]
    tokens = remove_sq_br(tokens)[0]

    # append occupation in correct coreference cluster 
    occs_correct_coref.append(tokens[correct_occ_idx])

# delete 's' from occupations
occs_correct_coref = [occ[:-1] if occ.endswith('s') else occ for occ in occs_correct_coref]
# count occurence of each occupation (*2 to count occurences in pro lines as well)
occs_correct_coref = Counter(occs_correct_coref*2)

#print results 
print('Occurance of each occupation in correct coreference pair')
print(occs_correct_coref)