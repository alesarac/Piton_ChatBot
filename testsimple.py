import simplenlg

lexicon = simplenlg.Lexicon.getDefaultLexicon()
nlgFactory = simplenlg.NLGFactory(lexicon)
phrase = simplenlg.SPhraseSpec(nlgFactory)
phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE, featureValue=simplenlg.InterrogativeType.WHY)

phrase.setTense(simplenlg.Tense.PAST)

phrase.setVerb("go")
phrase.setSubject("you")
phrase.setComplement("slow")

realizer = simplenlg.Realiser()
output = realizer.realiseSentence(phrase)
print(output)