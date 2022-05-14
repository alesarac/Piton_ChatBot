import spacy
from pathlib import Path
from spacy import displacy
from rapidfuzz.distance import Levenshtein
import time
import random

# TODO:
#  mettere il non urlare al caps lock
#  implementare il criterio di similarità
#  implementare il voto
#  come usare simpleNLG

# caricare la KB allenata in italiano "python -m spacy download it_core_news_md"
nlp = spacy.load("en_core_web_sm")
imageCounter = 0
ingredientePozione = "Criniera di Granian"

pozioniDict = {"pozione oculare": ["assenzio", "mandragora in umido", "corno di unicorno", "polvere blu"],
               "pozione tartagliante": ["valeriana", "acconito", "dittamo"]
               }


# serve per creare l'immagine del parsing
def displayParser(frase):
    global imageCounter
    imageCounter = imageCounter + 1
    svg = displacy.render(frase, style="dep")
    output_path = Path("./images/dependency_plot{0}.svg".format(imageCounter))
    output_path.open("w", encoding="utf-8").write(svg)


# serve per parsificare una frase data in input
def parser(fraseIngrediente):
    dict = {}
    for token in fraseIngrediente:
        dict[token.text] = [token.dep_, token.head.text, [child for child in token.children]]
        print(
            f"text={token.text},dep={token.dep_}, head_text={token.head.text},figli={[child for child in token.children]}")
    displayParser(nlp(fraseIngrediente))
    return dict


print("Ciao, sono Severus Piton")

haiStudiato = input("\nHai studiato?\n")

while True:
    if haiStudiato == 'si':
        print("Bene, allora possiamo procedere..")
        # time.sleep(2)
        pozione = random.choice(list(pozioniDict))
        ingrediente1 = input(
            "\nPrima partiamo con: "+pozione+"\nQuali sono i suoi ingredienti? scrivili uno per volta\n")
        if "?" in ingrediente1:
            print("Le domande le faccio io")
        else:
            dict = parser(nlp(ingrediente1))

            # controllo inanzitutto se nella risposta ci sia un'ingrediente che mi aspetto
            # altrimenti non mi metto manco ad analizzare la frase
            if ingredientePozione in dict:
                # controllo se ho scritto la parola 'ingrediente' all'interno della frase
                if "ingrediente" in dict:
                    # controllo se l'ingrediente nella frase dell'utente o la parola 'ingrediente' sia il soggetto
                    # della frase
                    if str(dict['ingrediente'][0]) == "nsubj" or str(dict[ingredientePozione][0]) == "nsubj":
                        print("OK, risposta corretta\n")
                        print("la parola ingrediente è: " + str(dict['ingrediente'][0]))
                        print("\nl' ingrediente è: " + dict[ingredientePozione][0])

                elif str(dict[ingredientePozione][0]) == "nsubj":
                    print("ok, l'ingrediente c'è nella frase ed è il soggetto")

                else:
                    print("mmh, hai detto l'ingrediente ma la frase è decontestualizzata..")
            else:
                print("La risposta non mi piace, non mi hai scritto l'ingrediente")
