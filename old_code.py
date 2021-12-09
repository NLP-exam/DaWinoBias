    # DEN UFAGLÆRTE
    
    '''
    if 'ufaglærte' in tokens:
        ufag_idx = tokens.index('ufaglærte')
        den_idx = tokens.index('ufaglærte')-1
        tokens[den_idx] = tokens[den_idx] + tokens[ufag_idx]
        print(ufag_idx, den_idx,tokens[den_idx])
        del tokens[ufag_idx]
    '''
    #Find idx of occupations
    '''
    for token in tokens: 
        if token in occupations:
            if token == 'ufaglærte':
                occ_idx.append(tokens.index(token)-1)
                sq_idx -= 1
            else:
                occ_idx.append(tokens.index(token))
    print('occ_idx',occ_idx)
    print('sq_idx',sq_idx)
    '''

# a document is a list of tokenized sentences
#doc = [["Lotte", "arbejder", "med", "Mads", "Emil","."], ["Hun", "er", "tandlæge", "."], ["Han", "er", "assistent"]]
#example = '[Udvikleren] diskuterede med designeren, fordi [hun] ikke kunne lide designet.'
#example2 = 'Udvikleren diskuterede med [designeren], fordi [hans] idé ikke kan blive implementeret.'
#example3 = 'Mekanikeren gav [kontorassistenten] en gave, fordi det var [hans] fødselsdag.'
