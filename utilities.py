# big KB
# import en_core_web_trf
import json
import random
from datetime import datetime
from pathlib import Path
from time import sleep

# small KB
import en_core_web_sm
import spacy
from spacy import displacy

imageCounter = 0
nlp = spacy.load("en_core_web_sm")
# dizionario globale delle pozioni
pozioni = {}


# caricare la KB allenata in italiano
def load_KB():
    global nlp
    nlp = en_core_web_sm.load()


# per caricare il JSON con le pozioni
def load_json():
    global pozioni
    with open('pozioni.json') as json_file:
        pozioni = json.load(json_file)


##########FUNZIONI DI UTILITA'######################################

# serve per creare l'immagine del parsing
def displayParser(frase):
    global imageCounter
    imageCounter = imageCounter + 1
    svg = displacy.render(frase, style="dep")
    output_path = Path("results_spacy.svg")
    output_path.open("w", encoding="utf-8").write(svg)


# serve a parsificare solo le dipendenze di una frase
def parser_oly_dep(frase):
    frase_parsata = nlp(frase)
    dict = {}
    for token in frase_parsata:
        dict[token.text] = token.dep_
        # print(f"text={token.text},dep={token.dep_}")
    # displayParser(frase_parsata)
    print(dict)
    return dict


# serve per parsificare le entity e vedere se nella frase c'è un nome proprio di persona
def parser_ne(frase):
    frase_parsata = nlp(frase)
    dict = {}
    for token in frase_parsata.ents:
        dict[token.text] = [token.text, token.start_char, token.end_char, token.label_]
        # print(f"text={token.text},inizio_stringa={token.start_char}, fine_stringa={token.end_char}, etichetta={token.label_}")
    for key, value in dict.items():
        if ("PERSON" in value):
            return key
    return None


def getTime():
    return int(datetime.now().strftime("%H"))


def loading():
    for i in range(1, 4):
        print(".", end='')
        sleep(0.3)
    print(".", end='\r')
    sleep(0.1)


# scelgo una pozione da chiedere all'untente in base alla dificoltà da 1 a 10
def selectPoison(difficoltà):
    while True:
        pozionicopia = pozioni
        pozione = random.choice(list(pozionicopia))
        if (pozionicopia[pozione][0] == difficoltà):
            pozioneScelta = {}
            pozioneScelta[pozione] = pozionicopia[pozione]
            break
    return pozioneScelta


def selectQuestion():
    lista = ("Ora parlami degli ingredienti di: ", "Invece adesso ti chiedo gli ingredienti della pozione chiamata: ",
             "Elencami gli ingredienti di: ")
    return random.choice(lista)


def checkScream(frase):
    if frase.isupper():
        print("\nNon urlare!\n")
        sleep(2)


def checkQuestion(frase):
    if "?" in frase:
        print("Le domande le faccio io!\n")
        sleep(2)


# da fare: deve ritornare true se sono entrambi passati, nel caso, uno false deve ripetere la cosa
def checkFrase(frase):
    checkScream(frase)
    checkQuestion(frase)
    return True


###### SPACY ######

'''# serve per parsificare le dipendenze di una frase data in input
def parser_dep(fraseIngrediente):
    frase_parsificata = nlp(fraseIngrediente)
    sent_dict = {}
    for token in frase_parsificata:
        print(token.text + ' : ' + str([token.dep_, token.head.text, [child for child in token.children]]))
        sent_dict[token.text] = [token.dep_, [child for child in token.children]]

    displayParser(frase_parsificata)
    return sent_dict


def get_ingredient(frase):
    sent = parser_def(frase.lower())
    print(sent)
    for tok in sent:
        # caso in cui l'ingrediente non è soggetto
        if tok == 'ingredient' and sent[tok][0] == 'nsubj':
            root_ingr = tok
        # caso in cui il soggetto è l'ingrediente
        elif tok == 'ingredient':
            root_ingr = tok
    return composed_ingredient(root_ingr, sent)
'''


def get_ingredient(frase):
    sent_dict = {}
    frase_parsificata = nlp(frase.lower())
    position = 'nsubj'
    for chunk in frase_parsificata.noun_chunks:
        #print(str(chunk) + ' - ' + str(chunk.root.dep_))
        # controlla dove si trova l'ingrediente, se è soggetto oppure complemento
        if 'ingredient' in chunk.text and chunk.root.dep_ == 'nsubj':
            position = 'attr'
        if chunk.root.dep_ == 'nsubj' or chunk.root.dep_ == 'attr':
            sent_dict[chunk.root.dep_] = chunk
    displayParser(frase_parsificata)

    return sent_dict[position]


def wrong_ingredient():
    sentences = [
        'Is this Avanti un Altro?! I\'m not Paolo Bonolis!',
        'Good answer... but it\'s wrong!',
        'That\'s a pity, try again'
    ]
    print(random.choice(sentences))


def check_ingredient(ingredient, list):
    if ingredient in list:
        return True
    else:
        wrong_ingredient()

# funzione per timeout attesa input
