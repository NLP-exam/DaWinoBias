from transformers import AutoTokenizer, AutoModelForPreTraining
from utility_fcs import load_texts, remove_sq_br
import torch, spacy, os

tokenizer = AutoTokenizer.from_pretrained("Maltehb/-l-ctra-danish-electra-small-uncased")
discriminator = AutoModelForPreTraining.from_pretrained("Maltehb/-l-ctra-danish-electra-small-uncased")

#load model used for tokenization
nlp = spacy.load("da_core_news_lg") 

#test set
anti_lines, pro_lines = [], []
path = os.path.join("NLP","Detecting-Bias-in--LMs","data")
anti_lines = load_texts(path,"anti", "both")
pro_lines = load_texts(path,"pro", "both")

# flatten lists
anti_lines = [sentence for sublist in anti_lines for sentence in sublist][0:1]
pro_lines = [sentence for sublist in pro_lines for sentence in sublist][0:1]

for anti_line, pro_line in zip(anti_lines, pro_lines): 
    # convert to nlp object
    anti_line_nlp = nlp(anti_line)

    # tokenize and lowercase
    fake_tokens = []
    for token in anti_line_nlp:
            fake_tokens.append(token.text.lower())
    
    fake_tokens = remove_sq_br(fake_tokens)
    #fake_tokens = tokenizer.tokenize(anti_line)

    fake_inputs = tokenizer.encode(anti_line, return_tensors="pt")
    discriminator_outputs = discriminator(fake_inputs)
    predictions = torch.round((torch.sign(discriminator_outputs[0]) + 1) / 2)

    [print("%7s" % token, end="\n") for token in fake_tokens]

    [print("%7s" % prediction, end="") for prediction in predictions.squeeze().tolist()]