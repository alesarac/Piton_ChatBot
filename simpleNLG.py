# inizializza la phrase con la libreria SimpleNLG
import utilities as util
import simplenlg


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
    return '\n' + output + '\n'


def printAskPotion(potion, ingredienti_pozione, domande_fatte, domande_pozione):
    lexicon = simplenlg.Lexicon.getDefaultLexicon()
    nlgFactory = simplenlg.NLGFactory(lexicon)
    '''What is the ingredient'''
    np_potion = nlgFactory.createNounPhrase("the", potion)
    np_ingredients = nlgFactory.createNounPhrase("the", "ingredient")
    proposition = nlgFactory.createClause(np_ingredients, "be")
    proposition.setFeature(simplenlg.Feature.INTERROGATIVE_TYPE, simplenlg.InterrogativeType.WHAT_OBJECT)
    ingredienti_mancanti = len(ingredienti_pozione)
    if ingredienti_mancanti == 1:
        '''What is the last ingredient?'''
        np_ingredients.addModifier("last")
    else:
        '''What are the ingredients?'''
        np_ingredients.setPlural(True)
        if domande_fatte == 0 and domande_pozione == 0:
            print(domande_fatte)
            '''Let's start with the potion, + What is the ingredient?'''
            output = realize_output(proposition)
            sentence = "Let's start with the " + potion + ', ' + output.lower()
            util.write_question(sentence)
            return sentence
        else:
            if domande_pozione > 0:
                return printAskIngredient(ingredienti_mancanti)
            else:
                '''What are the ingredients of the potion?'''
                np_potion.setSpecifier("of")
                np_ingredients.addModifier(np_potion)

    sentence = realize_output(proposition)
    util.write_question(sentence)
    return sentence


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

    np_ingr = nlgFactory.createNounPhrase("ingredient")
    if nIngredient > 1:
        np_ingr.setPlural(True)

    '''What are the other ingredients?'''
    np_ingredients = nlgFactory.createNounPhrase("the", "ingredient")
    np_ingredients.setPlural(True)
    np_ingredients.addModifier("other")
    continue_proposition = nlgFactory.createClause(np_ingredients, "be")
    continue_proposition.setFeature(simplenlg.Feature.INTERROGATIVE_TYPE, simplenlg.InterrogativeType.WHAT_OBJECT)

    sentence = realize_output(proposition) + realize_output(continue_proposition)
    util.write_question(sentence)
    return sentence


def printScore(score, casata_nome):
    """I award 5 points to Gryffindor"""
    lexicon = simplenlg.Lexicon.getDefaultLexicon()
    nlgFactory = simplenlg.NLGFactory(lexicon)

    np_casata = nlgFactory.createNounPhrase(casata_nome)
    np_casata.addPreModifier("to")
    np_points = nlgFactory.createNounPhrase("point")
    np_points.addPreModifier(str(score))
    proposition = nlgFactory.createClause("I", "award", np_points)
    proposition.addComplement(np_casata)

    if 1 < score < 0:
        np_points.setPlural(True)

    output = realize_output(proposition)
    return output


def start_exam():
    lexicon = simplenlg.Lexicon.getDefaultLexicon()
    nlgFactory = simplenlg.NLGFactory(lexicon)

    '''I'll ask you for the ingredients of 3 potions, then I'll give you a grade.'''
    np_ingredients = nlgFactory.createNounPhrase("the", "ingredient")
    np_ingredients.setPlural(True)
    np_ingredients.addModifier("of")
    np_potion = nlgFactory.createNounPhrase("potion")
    np_potion.setPlural(True)
    np_potion.addPreModifier("3")
    proposition = nlgFactory.createClause("I", "ask for", np_ingredients)
    proposition.addComplement(np_potion)
    proposition.setFeature(simplenlg.Feature.TENSE, simplenlg.Tense.FUTURE)

    output = realize_output(proposition)
    return output
