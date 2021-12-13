from transformers import AutoTokenizer, AutoModelForPreTraining, AutoModelForMaskedLM
from utility_fcs import idx_occ_pron, remove_sq_br, load_texts, get_pred_res
import torch, os

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

#mask pronouns in test set 
_, prons_ids = idx_occ_pron(anti_lines)
# create prompt:
for sentence in anti_lines: 
    sentence_to_classify = sentence 
    "I love working with NLP" 
prompt = f"""

{Sentence_before} [{tokenizer.mask_token}] {sentence_after}
"""

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