import simplenlg

lexicon = simplenlg.Lexicon.getDefaultLexicon()
nlgFactory = simplenlg.NLGFactory(lexicon)
phrase = simplenlg.SPhraseSpec(nlgFactory)

#Devi dirmi il tuo nome..
#you must tell me your name
phrase.setFeature(featureName=simplenlg.Feature.MODAL, featureValue="must")

phrase.setTense(simplenlg.Tense.PRESENT)
phrase.setFeature(featureName=simplenlg.LexicalFeature.REFLEXIVE, featureValue=simplenlg.)

phrase.setVerb("tell")
phrase.setObject("your")
phrase.setSubject("you")
phrase.setComplement("name")

realizer = simplenlg.Realiser()
output = realizer.realiseSentence(phrase)
print(output)