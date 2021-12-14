import os
from utility_fcs import load_texts, load_occs
from collections import Counter

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
_, occ_no_poss, _ = load_occs(female=True,male=True)
_, f_occ_no_poss, _ = load_occs(female=True)
_, m_occ_no_poss, _ = load_occs(male=True)

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
