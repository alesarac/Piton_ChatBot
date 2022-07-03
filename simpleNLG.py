import simplenlg

#inizializza la phrase con la libreria SimpleNLG
def init():
    lexicon = simplenlg.Lexicon.getDefaultLexicon()
    nlgFactory = simplenlg.NLGFactory(lexicon)
    phrase = simplenlg.SPhraseSpec(nlgFactory)
    return phrase

#costruisce una frase normale completa
def build_phrase_complete(soggetto,verbo,complemento):
    phrase=init()

    phrase.setFeature(featureName=simplenlg.Feature.FORM, featureValue=simplenlg.ABC)
    phrase.setTense(simplenlg.Tense.PRESENT)

    phrase.setVerb(verbo)
    phrase.setSubject(soggetto)
    phrase.setComplement(complemento)

    return relalize_output(phrase)

#costruisce una frase con solo un complemento
def build_phrase(complemento):
    phrase=init()

    phrase.setFeature(featureName=simplenlg.Feature.FORM, featureValue=simplenlg.ABC)
    phrase.setTense(simplenlg.Tense.PRESENT)

    phrase.setComplement(complemento)
    return relalize_output(phrase)

#costruisce una domanda
def build_question(text):
    phrase=init()

    phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE, featureValue=simplenlg.InterrogativeType.WHY)
    phrase.setTense(simplenlg.Tense.PRESENT)

    # phrase.setVerb("go")
    # phrase.setSubject("you")
    phrase.setComplement(text)
    return relalize_output(phrase)

def ask_info(complemento):
    phrase = init()

    phrase.setVerb("be")
    phrase.setObject("your")

    phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE, featureValue=simplenlg.InterrogativeType.WHAT_SUBJECT)
    phrase.setTense(simplenlg.Tense.PRESENT)

    phrase.setComplement(complemento)
    return relalize_output(phrase)

#def no_answer():

# stampa la frase costruita in uno dei metodi precedenti
def relalize_output(phrase):
    realizer = simplenlg.Realiser()
    output = realizer.realiseSentence(phrase)
    return output

import simplenlg

#inizializza la phrase con la libreria SimpleNLG
def init():
    lexicon = simplenlg.Lexicon.getDefaultLexicon()
    nlgFactory = simplenlg.NLGFactory(lexicon)
    phrase = simplenlg.SPhraseSpec(nlgFactory)
    return phrase

#costruisce una frase normale completa
def build_phrase_complete(soggetto,verbo,complemento):
    phrase=init()

    phrase.setFeature(featureName=simplenlg.Feature.FORM, featureValue=simplenlg.ABC)
    phrase.setTense(simplenlg.Tense.PRESENT)

    phrase.setVerb(verbo)
    phrase.setSubject(soggetto)
    phrase.setComplement(complemento)

    return relalize_output(phrase)

#costruisce una frase con solo un complemento
def build_phrase(complemento):
    phrase=init()

    phrase.setFeature(featureName=simplenlg.Feature.FORM, featureValue=simplenlg.ABC)
    phrase.setTense(simplenlg.Tense.PRESENT)

    phrase.setComplement(complemento)
    return relalize_output(phrase)

#costruisce una domanda
def build_question(text):
    phrase=init()

    phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE, featureValue=simplenlg.InterrogativeType.WHY)
    phrase.setTense(simplenlg.Tense.PRESENT)

    # phrase.setVerb("go")
    # phrase.setSubject("you")
    phrase.setComplement(text)
    return relalize_output(phrase)

def ask_info(complemento):
    phrase = init()

    phrase.setVerb("be")
    phrase.setObject("your")

    phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE, featureValue=simplenlg.InterrogativeType.WHAT_SUBJECT)
    phrase.setTense(simplenlg.Tense.PRESENT)

    phrase.setComplement(complemento)
    return relalize_output(phrase)

def no_answer(obj, complmentent):
    phrase = init()

    phrase.setFeature(featureName=simplenlg.Feature.MODAL, featureValue="must")

    phrase.setVerb("tell")
    phrase.setObject(obj)
    phrase.setSubject("you")
    phrase.setComplement(complmentent)
    phrase.setIndirectObject("me")

    return relalize_output(phrase)

def verb_subj(verb,subject):
    phrase = init()

    phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE, featureValue=simplenlg.InterrogativeType.YES_NO)
    phrase.setTense(simplenlg.Tense.PAST)
    phrase.setVerb(verb)
    phrase.setSubject(subject)

    return relalize_output(phrase)

#stampa la frase costruita in uno dei metodi precedenti
def relalize_output(phrase):
    realizer = simplenlg.Realiser()
    output = realizer.realiseSentence(phrase)
    return output
