import utilities as util
import time
import simpleNLG as sp

'''
    Carico la conoscenza base, le pozioni e setto la difficoltà di default
'''
util.load_KB()
util.load_json()
difficolta = 1

'''
    Decido, in base a che ora sia, se dire: "Buongiorno" o "Buonasera"
'''
if util.getTime() >= 12:
    print(sp.build_phrase("Good evening"))
elif 12 < util.getTime() >= 18:
    print(sp.build_phrase("Good afternoon"))
else:
    print(sp.build_phrase("Good morning"))
time.sleep(1)
print(sp.build_phrase_complete("I", "be", "Severus Piton") + "\n")
util.loading()

'''
    Parte relativa al riconoscimento del nome
'''
risposta_nome = input(sp.ask_info("name") + "\n")
util.loading()
util.checkFrase(risposta_nome)

nome = util.parser_ne(risposta_nome)

while nome is None or nome == '':
    util.loading()
    risposta_nome = input(sp.no_answer("your", "name") + "\n")
    nome = util.parser_ne(risposta_nome)
    '''controllo che la risposta è una frase, oppure il nome diretto'''

'''
    Parte relativa al riconosciemento della casata
'''
casata_nome = input("\n" + sp.ask_info("house") + "\n")
casata_nome = util.answer_casata(casata_nome)

while casata_nome is None or casata_nome == '':
    util.loading()
    casata_nome = input("\n" + sp.no_answer("your", "house"))
    casata_nome = util.parser_ne(casata_nome)

print(risposta_nome + ", " + sp.verb_subj("study", "you").lower())  # have you studied / did you study
haiStudiato = None
while haiStudiato is None or haiStudiato == '':
    haiStudiato = input()  # si potrebbe parsificare la frase (si ho studiato, no non ho studiato)
    util.checkFrase(haiStudiato)
    if 'not' in haiStudiato.lower() or '\'t' in haiStudiato.lower() or 'no' in haiStudiato.lower():
        haiStudiato = False
    elif 'yes' in haiStudiato.lower() or 'of course' in haiStudiato.lower() or 'i have studied' in haiStudiato.lower():
        haiStudiato = True
    else:
        print("Don't make fun of me! Tell me if you have studied!")

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

domande = 3
domande_fatte = 0
difficolta = 1

ingredienti_indovinati = []
pozioni_chieste = []
all_ingredienti = util.get_all_ingredients()
score = 0.0

while domande > domande_fatte:
    pozioneScelta_dict = util.selectPoison(difficolta)
    nome_pozione = str(list(pozioneScelta_dict.keys())[0])
    pozioni_chieste.append(nome_pozione)
    ingredienti_pozione = list(pozioneScelta_dict.values())[0][1]
    domande_pozione = 0

    while len(ingredienti_pozione) > 0 and domande_pozione < len(ingredienti_pozione) + 1:
        print('\n' + str(ingredienti_pozione))
        ingredienti_pozione_, domande_pozione_, score_ = util.ask_question(nome_pozione, domande_fatte,
                                                                           ingredienti_pozione,
                                                                           ingredienti_indovinati, difficolta,
                                                                           domande_pozione,
                                                                           False)
        domande_pozione = domande_pozione_
        ingredienti_pozione = ingredienti_pozione_
        score += float(score_)

    domande_fatte += 1
    difficolta += 1

print('Good, we finished the exam\n')

if score < 0:
    print(nome + ", you got it all wrong. " + sp.printScore(score, casata_nome) + "\n")
elif 10 <= score <= 22:
    print(nome + ", you could have done better. " + sp.printScore(score, casata_nome) + "\n")
else:
    print(nome + ", you have been very good. " + sp.printScore(score, casata_nome) + "\n")
