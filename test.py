from transformers import pipeline

model_name = "distilbert-base-uncased" # a small version of BERT

nlp = pipeline("fill-mask", model_name) # create pipeline

sentence_to_classify = "I love working with NLP"

prompt = f"""
I hate my life. => negative
The movie I saw yesterday was great! => positive
{sentence_to_classify} => {nlp.tokenizer.mask_token}
"""

print(prompt)
#print(nlp(prompt))