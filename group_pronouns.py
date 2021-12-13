def group_pronouns(pronouns): 
    '''group labels in female and male pronouns'''

    #define groups of pronouns
    female_pronouns = ['hun', 'hendes']
    male_pronouns = ['han', 'hans']

    #initialize lists
    group_pronoun= []

    #group labels
    for pronoun in pronouns: 
        if pronoun in female_pronouns: 
            group_pronoun.append('hun/hendes')
        elif pronoun in male_pronouns: 
            group_pronoun.append('han/hans')
        else:
            group_pronoun.append('UNK')
    
    return group_pronoun
