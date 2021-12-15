def remove_sq_br(tokens):
    """Remove square brackets from tokens

    Arguments:
        tokens {[type]} -- [tokenized line]

    Returns:
        [list] -- [tokenized line without square brackets]
    """    
    #input tokens to remove '[]' 
    return [[token for token in tokens if token != '[' and token != ']']]
