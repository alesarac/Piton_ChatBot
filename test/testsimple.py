import simplenlg

lexicon = simplenlg.Lexicon.getDefaultLexicon()
nlgFactory = simplenlg.NLGFactory(lexicon)
phrase = simplenlg.SPhraseSpec(nlgFactory)

#Devi dirmi il tuo nome..
#you must tell me your name
phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE, featureValue=simplenlg.InterrogativeType.YES_NO)

phrase.setTense(simplenlg.Tense.PAST)
#phrase.setFeature(featureName=simplenlg.LexicalFeature.REFLEXIVE, featureValue="dio porcoo")

phrase.setVerb("study")
phrase.setSubject("you")


realizer = simplenlg.Realiser()
output = realizer.realiseSentence(phrase)
print(output)