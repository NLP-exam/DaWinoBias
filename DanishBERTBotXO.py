from transformers import AutoTokenizer, AutoModelForPreTraining, AutoModelForMaskedLM, pipeline
from utility_fcs import idx_occ_pron, remove_sq_br, load_texts, get_pred_res
import torch, os, spacy

#load model used for tokenization
nlp = spacy.load("da_core_news_lg") 
#nlp = pipeline("fill-mask")
#print(nlp(f"HuggingFace is creating a {nlp.tokenizer.mask_token} that the community uses to solve NLP tasks."))

tokenizer = AutoTokenizer.from_pretrained("Maltehb/danish-bert-botxo")
model = AutoModelForPreTraining.from_pretrained("Maltehb/danish-bert-botxo")

#train set
lines = []
path = os.path.join("NLP","Detecting-Bias-in--LMs","data")
lines.append(load_texts(path,"anti", "dev"))
lines.append(load_texts(path,"pro", "dev"))

#test set 
anti_lines = load_texts(path,"anti", "dev")
pro_lines = load_texts(path,"pro", "dev")

# flatten lists
anti_lines = [sentence for sublist in anti_lines for sentence in sublist]
pro_lines = [sentence for sublist in pro_lines for sentence in sublist]

#mask pronouns in test set 
for line in anti_lines:
    #convert to nlp object
    line = nlp(line)

    #tokenize and lowercase
    tokens = []
    for token in line:
        tokens.append(token.text.lower())
    
    #find index of pronoun
    _, prons_idx = idx_occ_pron(tokens)

    #remove square brackets
    tokens = remove_sq_br(tokens)[0]

    #MASK pronouns
    tokens[prons_idx] = '[MASK]'

    #collected sentence
    sentence = ' '.join(tokens)
    print(sentence)

# create prompt:
for sentence in anti_lines: 
    sentence_to_classify = sentence 
    "I love working with NLP" 
#{Sentence_before} [{tokenizer.mask_token}] {sentence_af

nlp = pipeline("fill-mask", model_name) # create pipeline

sentence_to_classify = "I love working with NLP"

prompt = f"""
I hate my life. => negative
The movie I saw yesterday was great! => positive
{sentence_to_classify} => {nlp.tokenizer.mask_token}
"""

print(prompt)
print(nlp(prompt))

# tokenize the input
input = tokenizer.encode(prompt, return_tensors="pt")
mask_token_index = torch.where(input == tokenizer.mask_token_id)
mask_token_index = torch.where(input == tokenizer.mask_token_id)[1]  # record the index of the mask token

# forward pass through the model
token_logits = model(input).logits
token_logits.shape  # (batch_size, tokens, vocabulary) in this case it is (1, 30, 30522)

# extract the most likely word for the MASK
mask_token_logits = token_logits[0, mask_token_index, :]  # select the mask token
top_5_tokens = torch.topk(mask_token_logits, 5, dim=1).indices[0].tolist()

for token in top_5_tokens:
    print(tokenizer.decode([token]))
