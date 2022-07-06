import simplenlg


# inizializza la phrase con la libreria SimpleNLG
def init():
    lexicon = simplenlg.Lexicon.getDefaultLexicon()
    nlgFactory = simplenlg.NLGFactory(lexicon)
    phrase = simplenlg.SPhraseSpec(nlgFactory)
    return phrase


# costruisce una frase normale completa
def build_phrase_complete(soggetto, verbo, complemento):
    phrase = init()

    phrase.setFeature(featureName=simplenlg.Feature.FORM, featureValue=simplenlg.ABC)
    phrase.setTense(simplenlg.Tense.PRESENT)

    phrase.setVerb(verbo)
    phrase.setSubject(soggetto)
    phrase.setComplement(complemento)

    return realize_output(phrase)


# costruisce una frase con solo un complemento
def build_phrase(complemento):
    phrase = init()

    phrase.setFeature(featureName=simplenlg.Feature.FORM, featureValue=simplenlg.ABC)
    phrase.setTense(simplenlg.Tense.PRESENT)

    phrase.setComplement(complemento)
    return realize_output(phrase)


# costruisce una domanda
def build_question(text):
    phrase = init()

    phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE, featureValue=simplenlg.InterrogativeType.WHY)
    phrase.setTense(simplenlg.Tense.PRESENT)

    # phrase.setVerb("go")
    # phrase.setSubject("you")
    phrase.setComplement(text)
    return realize_output(phrase)


def ask_info(complemento):
    phrase = init()

    phrase.setVerb("be")
    phrase.setObject("your")

    phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE,
                      featureValue=simplenlg.InterrogativeType.WHAT_SUBJECT)
    phrase.setTense(simplenlg.Tense.PRESENT)

    phrase.setComplement(complemento)
    return realize_output(phrase)


# def no_answer():

# stampa la frase costruita in uno dei metodi precedenti
def relalize_output(phrase):
    realizer = simplenlg.Realiser()
    output = realizer.realiseSentence(phrase)
    return output


import simplenlg


# inizializza la phrase con la libreria SimpleNLG
def init():
    lexicon = simplenlg.Lexicon.getDefaultLexicon()
    nlgFactory = simplenlg.NLGFactory(lexicon)
    phrase = simplenlg.SPhraseSpec(nlgFactory)
    return phrase


# costruisce una frase normale completa
def build_phrase_complete(soggetto, verbo, complemento):
    phrase = init()

    phrase.setFeature(featureName=simplenlg.Feature.FORM, featureValue=simplenlg.ABC)
    phrase.setTense(simplenlg.Tense.PRESENT)

    phrase.setVerb(verbo)
    phrase.setSubject(soggetto)
    phrase.setComplement(complemento)

    return realize_output(phrase)


# costruisce una frase con solo un complemento
def build_phrase(complemento):
    phrase = init()

    phrase.setFeature(featureName=simplenlg.Feature.FORM, featureValue=simplenlg.ABC)
    phrase.setTense(simplenlg.Tense.PRESENT)

    phrase.setComplement(complemento)
    return realize_output(phrase)


# costruisce una domanda
def build_question(text):
    phrase = init()

    phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE, featureValue=simplenlg.InterrogativeType.WHY)
    phrase.setTense(simplenlg.Tense.PRESENT)

    # phrase.setVerb("go")
    # phrase.setSubject("you")
    phrase.setComplement(text)
    return realize_output(phrase)


def ask_info(complemento):
    phrase = init()

    phrase.setVerb("be")
    phrase.setObject("your")

    phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE,
                      featureValue=simplenlg.InterrogativeType.WHAT_SUBJECT)
    phrase.setTense(simplenlg.Tense.PRESENT)

    phrase.setComplement(complemento)
    return realize_output(phrase)


def no_answer(obj, complmentent):
    phrase = init()

    phrase.setFeature(featureName=simplenlg.Feature.MODAL, featureValue="must")

    phrase.setVerb("tell")
    phrase.setObject(obj)
    phrase.setSubject("you")
    phrase.setComplement(complmentent)
    phrase.setIndirectObject("me")

    return realize_output(phrase)


def verb_subj(verb, subject):
    phrase = init()

    phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE, featureValue=simplenlg.InterrogativeType.YES_NO)
    phrase.setTense(simplenlg.Tense.PAST)
    phrase.setVerb(verb)
    phrase.setSubject(subject)

    return realize_output(phrase)


# stampa la frase costruita in uno dei metodi precedenti
def realize_output(phrase):
    realizer = simplenlg.Realiser()
    output = realizer.realiseSentence(phrase)
    return output


def printAskPotion(potion, ingredienti_mancanti, domande_fatte):
    lexicon = simplenlg.Lexicon.getDefaultLexicon()
    nlgFactory = simplenlg.NLGFactory(lexicon)
    '''What is the ingredient'''
    np_potion = nlgFactory.createNounPhrase("the", potion)
    np_ingredients = nlgFactory.createNounPhrase("the", "ingredient")
    proposition = nlgFactory.createClause(np_ingredients, "be")
    proposition.setFeature(simplenlg.Feature.INTERROGATIVE_TYPE, simplenlg.InterrogativeType.WHAT_OBJECT)

    if ingredienti_mancanti == 1:
        '''What is the last ingredient?'''
        np_ingredients.addModifier("last")
    else:
        '''What are the ingredients?'''
        np_ingredients.setPlural(True)
        if domande_fatte != 1:
            '''What are the ingredients of the potion?'''
            np_potion.setSpecifier("of")
            np_ingredients.addModifier(np_potion)
        else:
            '''Let's start with the potion, + What is the ingredient?'''
            output = realize_output(proposition)
            print("Let's start with the potion, " + output.lower())

    output = realize_output(proposition)
    print(output)


def printAskIngredient(nIngredient):
    lexicon = simplenlg.Lexicon.getDefaultLexicon()
    nlgFactory = simplenlg.NLGFactory(lexicon)

    np_number = nlgFactory.createNounPhrase(str(nIngredient))
    np_ingredients = nlgFactory.createNounPhrase("ingredient")
    np_missing = nlgFactory.createNounPhrase("missing")
    np_ingredients.addPreModifier(np_number)
    proposition = nlgFactory.createClause(np_ingredients, "be", np_missing)
    if nIngredient > 1:
        np_ingredients.setPlural(True)
        proposition.setPlural(True)
        np_missing.setPlural(True)

    output = realize_output(proposition)

    print(output)
    np_ingr = nlgFactory.createNounPhrase("ingredient")
    if nIngredient > 1:
        np_ingr.setPlural(True)

    '''What are the other ingredients?'''
    np_ingredients = nlgFactory.createNounPhrase("the", "ingredient")
    np_ingredients.setPlural(True)
    np_ingredients.addModifier("other")
    continue_proposition = nlgFactory.createClause(np_ingredients, "be")
    continue_proposition.setFeature(simplenlg.Feature.INTERROGATIVE_TYPE, simplenlg.InterrogativeType.WHAT_OBJECT)

    output = realize_output(continue_proposition)
    print(output)
