from transformers import AutoTokenizer, AutoModelForPreTraining, AutoModelForMaskedLM, pipeline
import torch, os, spacy, random 
from collections import Counter

from utility_functions.idx_occupations_pronoun import idx_occ_pron
from utility_functions.remove_square_brackets import remove_sq_br
from utility_functions.load_data import load_texts
from utility_functions.predict_mask import predict_masked
from utility_functions.group_pronouns import group_pronouns
from utility_functions.model_evaluation import evaluate_model

#set seed 
torch.manual_seed(3)

#define model, pipeline and tokenizer
model = "Maltehb/danish-bert-botxo"
nlp =  pipeline(task = "fill-mask", model = model) 
tokenizer = spacy.load("da_core_news_lg") 

#load data set
anti_lines, pro_lines = [], []
path = os.path.join('data')
anti_lines = load_texts(path,'anti','both')
pro_lines = load_texts(path,'pro', 'both')

# flatten lists
anti_lines = [sentence for sublist in anti_lines for sentence in sublist]
pro_lines = [sentence for sublist in pro_lines for sentence in sublist]

# randomize data 
random.shuffle(anti_lines)
random.shuffle(pro_lines)

#mask and predict pronoun 
anti_labels, anti_preds = predict_masked(lines = anti_lines, nlp = nlp, tokenizer = tokenizer)
pro_labels, pro_preds = predict_masked(lines = pro_lines, nlp = nlp, tokenizer = tokenizer)

#group pronouns
anti_labels, anti_preds = group_pronouns(anti_labels),group_pronouns(anti_preds) 
pro_labels, pro_preds = group_pronouns(pro_labels),group_pronouns(pro_preds) 

#count number of pronoun predictions
anti_count_pronouns = Counter(anti_preds)
pro_count_pronouns = Counter(pro_preds)

print('anti_count_pronouns', anti_count_pronouns)
print('pro_count_pronouns', pro_count_pronouns)

#evaluate performance
evaluate_model(anti_labels, anti_preds, filename = 'results/danishbert_anti_results_mlm')
evaluate_model(pro_labels, pro_preds, filename = 'results/danishbert_pro_results_mlm')

print(evaluate_model(anti_labels, anti_preds, filename = 'results/danishbert_anti_results_mlm'))
print(evaluate_model(pro_labels, pro_preds, filename = 'results/danishbert_pro_results_mlm'))