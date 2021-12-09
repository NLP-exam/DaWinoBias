def remove_sq_br(tokens):
    #remove '[]'
    return [[token for token in tokens if token != '[' and token != ']']]

def idx_occ_pron(tokens):
    #define occupations, pronouns and '[]'
    occupations = ['chaufføren', 'supervisoren', 'viceværten', 'kokken', 'flyttemanden', 
    'den ufaglærte', 'entreprenøren', 'lederen', 'udvikleren', 'tømreren', 'manageren', 'advokaten', 
    'landmanden', 'sælgeren', 'lægen', 'vagten', 'analytikeren', 'mekanikeren', 'ceoen','kassedamen',
    'læreren','sygeplejerske','assistent','sekretæren','revisoren','rengøringsassistenten','receptionisten'
    ,'kontorassistenten','rådgiveren','designeren','frisøren','forfatteren','husholdersken','bageren','bogholderen'
    ,'redaktøren','bibliotekaren','syersken']
    pronouns = ['hans', 'hendes', 'han', 'hun']
    square_brackets = ['[']

    #empty lists
    occ_idx, sq_idx, prons_idx = [], [], []

    #find idx of pronouns 
    prons_idx = [[tokens.index(i) for i in pronouns if i in tokens][0] -3][0]

    #find correct referenced occupation in string
    sq_idx = [tokens.index(i) for i in square_brackets if i in tokens][0]
    
    #remove square brackets
    tokens = remove_sq_br(tokens)[0]

    #Find idx of occupations
    occ_idx = [tokens.index(i) for i in tokens if i in occupations] 

    #find the incorrect referenced occupations in string
    occ_idx.remove(sq_idx)

    #save correct and incorrect answer
    correct_cluster = [sq_idx, prons_idx]
    incorrect_cluster = [occ_idx[0], prons_idx]
    return [correct_cluster, incorrect_cluster]

