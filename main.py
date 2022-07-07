import utilities as util
import time
import simpleNLG as sp

# TODO:
#   1)Nomi alberto alessandro enrico
#   2)Quando risponde e che sia coerente con la domanda
#   4)Score, in base al voto ti da un giudizio ---DA CAMBIRE I VOTI E FARLI REALI---
#   5)Memory
#   6)Pulizia generale
#   7)Modificare l'interrogativa e fare controllo sulla negatività

'''
    Carico la conoscenza base, le pozioni e setto la difficoltà di default
'''
util.load_KB()
util.load_json()
difficolta = 3

'''
    Decido, in base a che ora sia, se dire: "Buongiorno" o "Buonasera"
'''
if util.getTime() >= 18:
    print(sp.build_phrase("Good evening"))
else:
    print(sp.build_phrase("Good morning"))
time.sleep(1)
print(sp.build_phrase_complete("I", "be", "Severus Piton"))
util.loading()

'''
    Parte relativa al riconoscimento del nome
'''
risposta_nome = input("\n" + sp.ask_info("name") + "\n")
util.loading()
util.checkFrase(risposta_nome)

nome = util.parser_ne(risposta_nome)
if nome == "":
    nome = None

while nome is None:
    util.loading()
    risposta_nome = input("\n" + sp.no_answer("your", "name") + "\n")
    nome = util.parser_ne(risposta_nome)
    '''controllo che la risposta è una frase, oppure il nome diretto'''

'''
    Parte relativa al riconosciemento della casata
'''
casata_nome = input("\n" + sp.ask_info("house") + "\n")
casata_nome = util.answer_casata(casata_nome)

print(f"\n{nome}" + ", " + sp.verb_subj("study", "you").lower())  # have you studied / did you study

haiStudiato = input()  # si potrebbe parsificare la frase (si ho studiato, no non ho studiato)
util.checkFrase(haiStudiato)
if 'not' in haiStudiato.lower() or '\'t' in haiStudiato.lower() or 'no' in haiStudiato.lower():
    haiStudiato = False
else:
    haiStudiato = True

if haiStudiato:
    util.loading()
    print("\nWell, now we will find out ..")
    time.sleep(1)
    print(sp.start_exam())
    time.sleep(2)
    util.loading()
else:
    util.loading()
    print("\nVery bad, see you next time!")
    time.sleep(2)
    exit()

domande = 2
domande_fatte = 0

ingredienti_indovinati = []
all_ingredienti = util.get_all_ingredients()
score = 0.0

while domande > domande_fatte:
    pozioneScelta_dict = util.selectPoison(difficolta)
    nome_pozione = str(list(pozioneScelta_dict.keys())[0])
    ingredienti_pozione = list(pozioneScelta_dict.values())[0][1]
    domande_pozione = 0

    while len(ingredienti_pozione) > 0 and domande_pozione < len(ingredienti_pozione) + 1:
        print(str(ingredienti_pozione))

        ingredienti_pozione_, domande_pozione_, score_ = util.ask_question(nome_pozione, domande_fatte,
                                                                           ingredienti_pozione,
                                                                           ingredienti_indovinati, difficolta,
                                                                           domande_pozione,
                                                                           False)
        domande_pozione = domande_pozione_
        ingredienti_pozione = ingredienti_pozione_
        score += float(score_)

    domande_fatte += 1
    difficolta -= 1

print('Good, we finished the exam\n')

if score == 0:
    print("You got it all wrong, your score is: " + sp.printScore(score, casata_nome) + "\n")
elif 1 < score < 5:
    print("You could have done better, your score is: " + sp.printScore(score, casata_nome) + "\n")
else:
    print("You have been very good, your score is: " + sp.printScore(score, casata_nome) + "\n")

