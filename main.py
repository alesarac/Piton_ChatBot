import utilities as util
from rapidfuzz.distance import Levenshtein
import time
import simpleNLG as sp

# TODO:

# mettere una difficoltà alle pozioni (fatto)
# implementare il criterio di similarità
# implementare il voto
# mettere un comando di uscita

# carico la conoscenza base, le pozioni e setto la difficoltà di default
util.load_KB()
util.load_json()
difficolta = 5

# decido, in base a che ora sia, se dire: "Buongiorno" o "Buonasera"
if util.getTime() >= 18:
    print(sp.build_phrase("Good evening"))
else:
    print(sp.build_phrase("Good morning"))
time.sleep(1)
print(sp.build_phrase_complete("I", "be", "Severus Piton"))
util.loading()

# parte relativa al riconoscimento del nome
risposta_nome = input("\n" + sp.ask_info("name") + "\n")
casata_nome = input("\n" + sp.ask_info("house") + "\n")
if len(risposta_nome.split()) == 1:
    nome = risposta_nome
else:
    nome = util.parser_ne(risposta_nome)
util.loading()
util.checkFrase(risposta_nome)
util.checkFrase(casata_nome)

while nome is None:
    util.loading()
    risposta_nome = input("\n" + sp.no_answer("your", "name") + "\n")
    # controllo che la risposta è una frase, oppure il nome diretto
print(f"\n{nome}" + ", " + sp.verb_subj("study", "you").lower())  # have you studied / did you study

haiStudiato = input()  # si potrebbe parsificare la frase (si ho studiato, no non ho studiato)
util.checkFrase(haiStudiato)
if 'not' in haiStudiato.lower() or '\'t' in haiStudiato.lower() or 'no' in haiStudiato.lower():
    haiStudiato = False
else:
    haiStudiato = True

if haiStudiato:
    util.loading()
    # qui c'è da richiamare SimpleNLG e fargli creare la frase nella print in inglese
    print("\nWell, now we will find out ..")
    time.sleep(1)
    # qui c'è da richiamare SimpleNLG e fargli crrare la frase nella print in inglese
    print("Ti chiederò gli ingredienti di 3 pozioni, e poi ti darò un voto.\n")
    time.sleep(2)
    util.loading()
else:
    util.loading()
    # qui c'è da richiamare SimpleNLG e fargli crrare la frase nella print in inglese
    print("\nVery bad, see you next time!")
    time.sleep(2)
    exit()

domande = 2
domande_fatte = 0

ingredienti_indovinati = []
all_ingredienti = util.get_all_ingredients()
score = 0

while domande > domande_fatte:
    pozioneScelta_dict = util.selectPoison(difficolta)
    nome_pozione = str(list(pozioneScelta_dict.keys())[0])
    ingredienti_pozione = list(pozioneScelta_dict.values())[0][1]
    domande_pozione = len(ingredienti_pozione) + 1

    while len(ingredienti_pozione) > 1 or domande_pozione > 1:
        domande_pozione -= 1
        print(str(domande_pozione) + 'domande pozione')
        ingredienti_pozione, score_ = util.ask_question(nome_pozione, domande_fatte, ingredienti_pozione,
                                                        ingredienti_indovinati, difficolta,
                                                        False)
        score += score_


    print(score)
    domande_fatte += 1
    difficolta = 3

print('Good, we finished the exam')
print('Scores')

'''
if haiStudiato:
    util.loading()
    # qui c'è da richiamare SimpleNLG e fargli creare la frase nella print in inglese
    print("\nBene, ora lo scopriremo..")
    time.sleep(1)
    # qui c'è da richiamare SimpleNLG e fargli crrare la frase nella print in inglese
    print("Ti chiederò gli ingredienti di 3 pozioni, e poi ti darò un voto.\n")
    time.sleep(2)
    util.loading()
else:
    util.loading()
    # qui c'è da richiamare SimpleNLG e fargli crrare la frase nella print in inglese
    print("\nMolto male, ci vediamo la prossima volta!")
    time.sleep(2)
    exit()




    print("Siamo alla domanda numero: " + str(domande_fatte + 1))
   # print("La difficoltà attuale è: " + str(difficolta))
   # scelgo la prima domanda (che è un dizionario (quindi il nostro fram è un dizionario che contiene una pozione alla volta) con solo una pozione all'interno
   # all'inizio "difficoltà" sarà quella di default, cioè 5
   # poi cambierà ad ogni cilo in base alle risposte date dall'utente
   # print("pozioneScelta_dict init: " + str(pozioneScelta_dict))
   pozioneScelta_dict = util.selectPoison(difficolta)

   # print("pozioneScelta_dict:" + str(pozioneScelta_dict))

   nome_pozione = str(list(pozioneScelta_dict.keys())[0])

   # print("nome_pozione attuale: " + str(nome_pozione))

   ingredienti_pozione = list(pozioneScelta_dict.values())[0]
   if domande_fatte == 1:
       ingredienti_indovinati = []

   # cancello la difficoltà dalla lista di ingredienti
   ingredienti_pozione.pop(0)

   # print("ingredienti_pozione attuale: " + str(ingredienti_pozione))

   time.sleep(1)

   # la prima volta dice "Partiamo" poi dopo cicla su delle frasi diverse
   # anche qua c'è da usare SimpleNLG per costruire ste frasi
   
       
       
    #if util.checkFrase(risposta):
    print(util.get_ingredient(risposta))

    # da qua in poi è tutto da rivedere nel senso che c'è da capire come accettiamo una risposta la mia idea è di
    # accettare una risposta che abbia come soggetto l'ingrediente e basta, ma è fin troppo semplice come condizione
       
       '''
