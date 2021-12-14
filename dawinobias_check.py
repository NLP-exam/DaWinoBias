from utility_fcs import load_texts

# load data 
path = os.path.join("nlp","Detecting-Bias-in--LMs","data")
anti_lines = load_texts(path,"anti", "both")
pro_lines = load_texts(path,"pro", "both")

print(anti_lines)
# check how many times each occupation is present in data 


# get count of how many female vs. male stereotypical occupations



# check position? 

