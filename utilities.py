import queue
import threading
from pathlib import Path
import random
from time import sleep

import spacy
from spacy import displacy
from datetime import datetime
# small KB
import en_core_web_sm
# big KB
# import en_core_web_trf
import json
import simpleNLG

imageCounter = 0
nlp = None
# dizionario globale delle pozioni
pozioni = {}
spacy.load('en_core_web_sm')


# caricare la KB allenata in italiano
def load_KB():
    global nlp
    '''Ricordarsi di mettere la kb più grossa'''
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
    output_path = Path("result_spacy.svg".format(imageCounter))
    output_path.open("w", encoding="utf-8").write(svg)


# serve per parsificare le dipendenze di una frase data in input
def parser_dep(fraseIngrediente):
    frase_parsata = nlp(fraseIngrediente)
    dict = {}
    for token in frase_parsata:
        dict[token.text] = [token.dep_, token.head.text, [child for child in token.children]]
        print(
            f"text={token.text},dep={token.dep_}, head_text={token.head.text}, figli={[child for child in token.children]}")
    displayParser(frase_parsata)
    return dict


# serve a parsificare solo le dipendenze di una frase
def parser_oly_dep(frase):
    frase_parsata = nlp(frase)
    dict = {}
    for token in frase_parsata:
        dict[token.text] = token.dep_
        # print(f"text={token.text},dep={token.dep_}")
    # displayParser(frase_parsata)
    return dict


# serve per parsificare le entity e vedere se nella frase c'è un nome proprio di persona
def parser_ne(frase):
    frase_parsata = nlp(frase)
    dict = {}
    for token in frase_parsata.ents:
        dict[token.text] = [token.text, token.start_char, token.end_char, token.label_]
        # print(f"text={token.text},inizio_stringa={token.start_char}, fine_stringa={token.end_char}, etichetta={
        # token.label_}")
    for key, value in dict.items():
        if "PERSON" in value:
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
        if pozionicopia[pozione][0] == difficoltà:
            pozioneScelta = {pozione: pozionicopia[pozione]}
            break
    return pozioneScelta


def get_all_ingredients():
    load_json()
    ingredients = []
    for p in pozioni:
        for ingredient in pozioni[p][1]:
            if ingredient not in ingredients:
                ingredients.append(ingredient.lower())
    return ingredients


def selectQuestion():
    lista = ("Ora parlami degli ingredienti di: ", "Invece adesso ti chiedo gli ingredienti della pozione chiamata: ",
             "Elencami gli ingredienti di: ")
    return random.choice(lista)


def checkScream(frase):
    if frase.isupper():
        print("\nDon't scream!\n")
        sleep(2)


def checkQuestion(frase):
    if "?" in frase:
        print("I ask the questions!\n")
        sleep(2)


def checkFrase(frase):
    checkScream(frase)
    checkQuestion(frase)


def ask_question(pozione, domande_fatte, ingredienti_pozione, ingredienti_indovinati, difficolta, aiuto, again):
    if not aiuto:
        if domande_fatte == 0:
            risposta = input(
                simpleNLG.printAskPotion(pozione, ingredienti_pozione, domande_fatte))
        else:
            risposta = input(simpleNLG.printAskPotion(pozione, ingredienti_pozione, domande_fatte))
    elif again:
        f = open("answers_memory.txt", "r")
        print(f.read())
    else:
        ingrediente = random.choice(get_all_ingredients())

        risposta_giusta = 'no'
        if ingrediente in [ingr.lower() for ingr in ingredienti_pozione]:
            risposta_giusta = 'yes'

        risposta = str(input(ingrediente + ' is an ingredient of ' + pozione + '?\n')).lower()
        if risposta == risposta_giusta:
            print('Correct')
            score = difficolta * len(ingrediente.split()) / 2
            return ingredienti_pozione, float(score)
        else:
            wrong_ingredient()
            return ingredienti_pozione, 0

    risposta = str(get_ingredient(risposta, False))
    if risposta == '' or 'repeat' in risposta or 'again' in risposta:
        ask_question(pozione, domande_fatte, ingredienti_pozione, ingredienti_indovinati, difficolta, False, True)
    ingredienti_pozione, is_correct = check_ingredient(risposta, ingredienti_pozione)

    if is_correct:
        return ingredienti_pozione, difficolta * len(risposta.split())
    else:
        wrong_ingredient()
        return ask_question(pozione, domande_fatte, ingredienti_pozione, ingredienti_indovinati, difficolta, True,
                            False)


##### SPACY ####

def get_ingredient(frase, aiuto):
    if aiuto:
        return
    sent_dict = {}
    frase_parsificata = nlp(frase)
    position = 'nsubj'
    for chunk in frase_parsificata.noun_chunks:
        print(chunk, chunk.root.dep_)
        # print(str(chunk) + ' - ' + str(chunk.root.dep_))
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
    return


def check_ingredient(ingrediente, ingredienti):
    print(ingrediente, ingredienti)
    if ingrediente in ingredienti:
        print("Correct!\n")
        simpleNLG.printAskIngredient(len(ingredienti))
        ingredienti.remove(ingrediente)
        return ingredienti, True
    else:
        return ingredienti, False

# funzione per timeout attesa input