"""import simplenlg

lexicon = simplenlg.Lexicon.getDefaultLexicon()
nlgFactory = simplenlg.NLGFactory(lexicon)
phrase = simplenlg.SPhraseSpec(nlgFactory)

#Devi dirmi il tuo nome..
#you must tell me your name

phrase.setFeature(featureName=simplenlg.Feature.MODAL, featureValue="must")

phrase.setTense(simplenlg.Tense.PRESENT)
# phrase.setFeature(featureName=simplenlg.LexicalFeature.REFLEXIVE, featureValue=simplenlg.)

phrase.setVerb("tell")
phrase.setObject("your")
phrase.setSubject("you")
phrase.setComplement("name")

phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE, featureValue=simplenlg.InterrogativeType.YES_NO)

phrase.setTense(simplenlg.Tense.PAST)
#phrase.setFeature(featureName=simplenlg.LexicalFeature.REFLEXIVE, featureValue="dio porcoo")

phrase.setVerb("study")
phrase.setSubject("you")



realizer = simplenlg.Realiser()
output = realizer.realiseSentence(phrase)
print(output)"""

import simplenlg

realiser = simplenlg.Realiser()


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

    output = realiser.realiseSentence(proposition)
    print(output)
    np_ingr = nlgFactory.createNounPhrase("the", "other one")
    if nIngredient > 1:
        np_ingr.setPlural(True)

    continue_proposition = nlgFactory.createClause("you", "nominate", np_ingr)
    continue_proposition.setFeature(simplenlg.Feature.MODAL, "can")
    continue_proposition.setFeature(simplenlg.Feature.INTERROGATIVE_TYPE, simplenlg.InterrogativeType.YES_NO)
    output = realiser.realiseSentence(continue_proposition)
    print(" " + output)


printAskIngredient(0)
