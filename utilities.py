from pathlib import Path
import random
from time import sleep
from spacy import displacy
from datetime import datetime
#small KB
import en_core_web_sm
#big KB
#import en_core_web_trf
import json

imageCounter=0
nlp = None
#dizionario globale delle pozioni
pozioni = {}

#caricare la KB allenata in italiano
def load_KB():
    global nlp
    nlp = en_core_web_sm.load()

#per caricare il JSON con le pozioni
def load_json():
    global pozioni
    with open('pozioni.json') as json_file:
        pozioni = json.load(json_file)

##########FUNZIONI DI UTILITA'######################################

#serve per creare l'immagine del parsing
def displayParser(frase):
    global imageCounter
    imageCounter=imageCounter+1
    svg = displacy.render(frase, style="dep")
    output_path = Path("./images/dependency_plot{0}.svg".format(imageCounter))
    output_path.open("w", encoding="utf-8").write(svg)

#serve per parsificare le dipendenze di una frase data in input
def parser_dep(fraseIngrediente):
    frase_parsata=nlp(fraseIngrediente)
    dict = {}
    for token in frase_parsata:
        dict[token.text]=[token.dep_,token.head.text,[child for child in token.children]]
        print(f"text={token.text},dep={token.dep_}, head_text={token.head.text}, figli={[child for child in token.children]}")
    displayParser(frase_parsata)
    return dict

#serve a parsificare solo le dipendenze di una frase
def parser_oly_dep(frase):
    frase_parsata=nlp(frase)
    dict = {}
    for token in frase_parsata:
        dict[token.text]=token.dep_
        #print(f"text={token.text},dep={token.dep_}")
    #displayParser(frase_parsata)
    return dict

#serve per parsificare le entity e vedere se nella frase c'è un nome proprio di persona
def parser_ne(frase):
    frase_parsata=nlp(frase)
    dict = {}
    for token in frase_parsata.ents:
        dict[token.text]=[token.text, token.start_char, token.end_char, token.label_]
        #print(f"text={token.text},inizio_stringa={token.start_char}, fine_stringa={token.end_char}, etichetta={token.label_}")
    for key, value in dict.items():
        if("PERSON" in value):
            return key
    return None

def getTime():
    return int(datetime.now().strftime("%H"))

def loading():
    for i in range(1,4):
        print(".", end='')
        sleep(0.8)
    print(".", end='\r')
    sleep(0.5)

#scelgo una pozione da chiedere all'untente in base alla dificoltà da 1 a 10
def selectPoison(difficoltà):
    while True:
        pozionicopia=pozioni
        pozione=random.choice(list(pozionicopia))
        if (pozionicopia[pozione][0]==difficoltà):
            pozioneScelta = {}
            pozioneScelta[pozione]=pozionicopia[pozione]
            break
    return pozioneScelta

def selectQuestion():
    lista = ("Ora parlami degli ingredienti di: ", "Invece adesso ti chiedo gli ingredienti della pozione chiamata: ", "Elencami gli ingredienti di: ")
    return random.choice(lista)

def checkScream(frase):
    if (frase.isupper()):
        print("\nNon urlare!\n")
        sleep(2)
def checkQuestion(frase):
    if ("?" in frase):
        print("Le domande le faccio io!\n")
        sleep(2)

def checkFrase(frase):
    checkScream(frase)
    checkQuestion(frase)