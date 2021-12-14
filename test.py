from transformers import ElectraForPreTraining, ElectraTokenizerFast
import torch

discriminator = ElectraForPreTraining.from_pretrained("google/electra-small-discriminator")
tokenizer = ElectraTokenizerFast.from_pretrained("google/electra-small-discriminator")

# two examples
s1 = "he is handsome"
s2 = "she is handsome"
s3 = "he went on a walk with his cat" # test sentence

input_ = tokenizer([s1, s2, s3], return_tensors="pt", padding=True)
discriminator_outputs = discriminator(**input_) #The ** operator allows us to take a dictionary of key-value pairs and unpack it into keyword arguments in a function call


tokenizer.tokenize([s1, s2])
# the tokenization:
#['he', 'is', 'handsome',
#'she', 'is', 'handsome']

tokenizer.decode(input_.input_ids[0])
# '[CLS] he is handsome [SEP] [PAD] [PAD] [PAD] [PAD] [PAD]'
tokenizer.decode(input_.input_ids[1])
# '[CLS] she is handsome [SEP] [PAD] [PAD] [PAD] [PAD] [PAD]'

# extract logits
output = discriminator_outputs.logits
output
# tensor([[-10.9578,  -2.9773,  -4.0094,  -0.5548, -11.0255,  14.4660,  14.7748,
#           14.6535,  14.8048,  14.6880],
#         [-10.3357,  -2.4011,  -3.3161,  -1.7713, -10.4259,  14.1202,  14.7713,
#           14.6626,  14.9124,  14.7328],
#         [-10.2929,  -3.1246,  -5.1340,  -2.8057,  -5.2957,  -3.5266,  -5.0109,
#           -3.1752,  -1.5812, -10.2848]], grad_fn=<SqueezeBackward1>)
# ignore the values of padding, CLS, and SEP tokens

output[0:2, 1]# første ord he/she (0 er CLS token)
# tensor([-2.9773, -2.4011], grad_fn=<SelectBackward>)
# she seems 'slightly' more likely to to be a replacement
# however handsome is more unlikely to be a replacement in the context of man.
output[0:2, 3] # handsome
# tensor([-0.5548, -1.7713], grad_fn=<SelectBackward>)

output[2, -2] # cat - probably most inlikely word in the sentence.
# tensor(-1.5812, grad_fn=<SelectBackward>)