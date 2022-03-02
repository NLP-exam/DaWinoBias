# DaWinoBias: Assessing Occupational Gender Stereotypes in Danish NLP Models

This is the repository for our, Kiri Koppelgaard and Signe Kirk Brødbæk's, NLP exam at MSc in Information Technology (Cognitive Science) at Aarhus University. 

# Abstract 
In the present paper, we introduce DaWinoBias, a Danish version of Type I sentences adapted from WinoBias by Zhao et al. (2018). Expanding on the application of WinoBias, we employ DaWinoBias to investigate three different transformer-based models for occupational gender bias in three different tasks. We utilise DaWinoBias to assess these biases both intrinsically and extrinsically, i.e. in two pre-trained models, DanishBERT and Ælæctra, as well as in a fine-tuned model, DaNLP's coreference model. We find that the performance of the coreference model from DaNLP does not differ in the pro-stereotypical and anti-stereotypical context. For DanishBERT in the fill mask task, we find that it has a slightly higher accuracy in a pro-stereotypical context, indicating a marginal occupational gender bias. Additionally, the model mainly predicts male pronouns. Similarly, when evaluating Ælæctra on a replaced token task, we infer a marginal intrinsic occupational gender bias as measured by DaWinoBias. Moreover, we find that the model predicts the female pronoun to be the replaced token much more than the male pronoun. However, one must be aware of limitations such as the notion that DaWinoBias solely investigates an occupational gender bias, and that it is based on American occupational stereotypes, which might not translate to a Danish context. With this corpus, we hope to increase awareness of the problem of occupational gender stereotypes within Danish NLP systems, as well as the need for evaluations going beyond held-out accuracy.

Key words: Danish NLP, DaWinoBias, WinoBias, Ælæctra, DanishBERT, conference resolution

# To run this code
* pip install -r requirements.txt
* python -m spacy download da_core_news_lg 
* python -m nltk.downloader all
