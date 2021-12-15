from transformers import AutoTokenizer, AutoModelForPreTraining
import torch, spacy, os
from collections import Counter
import random

from utility_functions.load_data import load_texts
from utility_functions.remove_square_brackets import remove_sq_br
from utility_functions.group_pronouns import group_pronouns

#set seed 
torch.manual_seed(4)

#load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("Maltehb/-l-ctra-danish-electra-small-uncased")
discriminator = AutoModelForPreTraining.from_pretrained("Maltehb/-l-ctra-danish-electra-small-uncased")

#define pronouns
pronouns = ['hans', 'han', 'ham', 'hendes', 'hun', 'hende']

#initialise results list
results = []
results_pronouns = []

#load data
anti_lines, pro_lines = [], []
path = os.path.join("data")
anti_lines = load_texts(path,"anti", "both")
pro_lines = load_texts(path,"pro", "both")

# flatten lists
anti_lines = [sentence for sublist in anti_lines for sentence in sublist]
pro_lines = [sentence for sublist in pro_lines for sentence in sublist]

# randomize data 
combined = list(zip(anti_lines, pro_lines))
random.shuffle(combined)
anti_lines[:], pro_lines[:] = zip(*combined)

for anti_line, pro_line in zip(anti_lines, pro_lines):
        #create input
        input_ = tokenizer([anti_line, pro_line], return_tensors="pt", padding=True)
        
        #tokenize sentences 
        anti_line = tokenizer.tokenize(anti_line)
        pro_line = tokenizer.tokenize(pro_line)

        #remove brackets 
        anti_line = remove_sq_br(anti_line)[0]
        pro_line = remove_sq_br(pro_line)[0]

        #extract pronoun position (+1 due to [CLS] in beginning of line)
        anti_pronoun_pos=[anti_line.index(i)+1 for i in anti_line if i in pronouns]
        pro_pronoun_pos=[pro_line.index(i)+1 for i in pro_line if i in pronouns]

        #predict odd-one-out
        discriminator_outputs = discriminator(**input_)

        # extract logits
        output  = discriminator_outputs.logits

        #Extract relevant probability for pronoun
        anti_output = output[0:1, anti_pronoun_pos]
        pro_output = output[1:2, pro_pronoun_pos]

        #If difference larger than 0.01, append the most likely
        if anti_output > pro_output and abs(anti_output - pro_output) >= 0.001: 
                results.append('anti')
        elif pro_output > anti_output and abs(anti_output - pro_output) >= 0.001: 
                results.append('pro')

        #Does the model in general predict 'han' as more likely?
        if anti_output > pro_output and abs(anti_output - pro_output) >= 0.001: 
                results_pronouns.append(anti_line[anti_pronoun_pos[0]-1])
        if pro_output > anti_output and abs(anti_output - pro_output) >= 0.001: 
                results_pronouns.append(pro_line[pro_pronoun_pos[0]-1])


#Count number of pro-stereotypical vs. anti-stereotypical
dist_results = Counter(results)
print(dist_results)

#calculate percentage of pro-stereotypical predictions and anti-stereotypical predictions
anti_percentage = round(dist_results['anti']/(dist_results['pro']+dist_results['anti']), 3)
pro_percentage = round(dist_results['pro']/(dist_results['pro']+dist_results['anti']), 3)

#group pronouns
results_pronouns = group_pronouns(results_pronouns)

#Count number of times 'hun' and 'han'is predicted as most likely, respectively
dist_results_pronouns = Counter(results_pronouns)
print(dist_results_pronouns)
#calculate percentage of 'hun' and 'han'is predicted as most likely, respectively
hun_percentage = round(dist_results_pronouns['hun/hendes']/(dist_results_pronouns['hun/hendes']+dist_results_pronouns['han/hans']),3)
han_percentage = round(dist_results_pronouns['han/hans']/(dist_results_pronouns['hun/hendes']+dist_results_pronouns['han/hans']),3)

#print results
print('anti_percentage', anti_percentage)
print('pro_percentage', pro_percentage)

print('han', han_percentage)
print('hun', hun_percentage)