import utilities as util
from rapidfuzz.distance import Levenshtein
import time
import simpleNLG as sp

# TODO:
# mettere il non urlare al caps lock (fatto)
# mettere una difficoltà alle pozioni (fatto)
# implementare il criterio di similarità
# implementare il voto
# come usare simpleNLG
# mettere un comando di uscita

# carico la conoscenza base di Italiano, le pozioni e setto la difficoltà di default
util.load_KB()
util.load_json()
difficolta = 5
#commento di prova

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

util.loading()
util.checkFrase(risposta_nome)
nome = util.parser_ne(risposta_nome)
while nome is None:
    util.loading()
    risposta_nome = input("\n" + sp.no_answer("your", "name") + "\n")
    nome = util.parser_ne(risposta_nome)
print(f"\n{nome}" + ", " + sp.verb_subj("study", "you").lower())  # have you studied / did you study

haiStudiato = input()
util.checkFrase(haiStudiato)

if haiStudiato.lower() == 'si':
    util.loading()
    print("\nBene, ora lo scopriremo..")
    time.sleep(1)
    print("Ti chiederò gli ingredienti di 3 pozioni, e poi ti darò un voto.\n")
    time.sleep(2)
    util.loading()
else:
    util.loading()
    print("\nMolto male, ci vediamo la prossima volta!")
    time.sleep(2)
    exit()

domande = 3

while domande > 0:

    print("Siamo alla domanda numero: " + str(domande))
    print("La difficoltà attuale è: " + str(difficolta))
    # scelgo la prima domanda (che è un dizionario con solo una pozione all'interno
    # all'inizio "difficoltà" sarà quella di default, cioè 5
    # poi cambierà ad ogni cilo in base alle risposte date dall'utente
    pozioneScelta_dict = {}
    print("pozioneScelta_dict init: " + str(pozioneScelta_dict))
    pozioneScelta_dict = util.selectPoison(difficolta)
    print("pozioneScelta_dict_dopo:" + str(pozioneScelta_dict))

    nome_pozione = str(list(pozioneScelta_dict.keys())[0])
    print("nome_pozione: " + str(nome_pozione))

    ingredienti_pozione = list(pozioneScelta_dict.values())[0]
    # cancello la difficoltà dalla lista di ingredienti
    ingredienti_pozione.pop(0)
    print("ingredienti_pozione: " + str(ingredienti_pozione))
    time.sleep(2)

    # la prima volta dice "Partiamo" poi dopo cicla su delle frasi diverse
    if domande == 3:
        risposta = input(f"\nPartiamo con: {nome_pozione}\nQuali sono i suoi ingredienti? (Scrivili uno per volta)\n")
        util.checkFrase(risposta)
    else:
        risposta = input(util.selectQuestion() + nome_pozione + ". (Scrivili uno per volta)\n")
        util.checkFrase(risposta)

    # controllo inanzitutto se nella risposta scritta al bot ci sia un'ingrediente che mi aspetto
    # altrimenti non mi metto manco ad analizzare la frase

    # da qua in poi è tutto da rivedere
    if risposta in ingredienti_pozione:
        rispostaParsata = util.parser_dep(risposta)
        print("l'ingrediente è nella risposta")
        # controllo se ho scritto la parola 'ingrediente' all'interno della risposta scritta al bot
        if "ingrediente" in risposta:
            # controllo se l'ingrediente nella frase dell'utente o la parola 'ingrediente' sia il soggetto della frase
            print("la parola 'ingrediente' è nella risposta'")
        # if(str(rispostaParsata['ingrediente'][0]) == "nsubj" or str(rispostaParsata[ingredientePozione][0]) ==
        # "nsubj"): print("OK, risposta corretta\n")

        # elif(str(dict[ingredientePozione][0]) == "nsubj"):
        # print("ok, l'ingrediente c'è nella frase ed è il soggetto")
        else:
            print("mmh, hai detto l'ingrediente ma la frase è decontestualizzata..")
    else:
        print("La risposta non mi piace, non mi hai scritto l'ingrediente")

    domande = domande - 1
    difficolta = 3
