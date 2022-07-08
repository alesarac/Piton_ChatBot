import pickle
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
import simpleNLG as sp

imageCounter = 0
nlp = None

# dizionario globale delle pozioni
pozioni = {}
spacy.load('en_core_web_sm')

with open('memory/questions.txt', 'wb') as f:
    pickle.dump([], f)

with open('memory/answers.txt', 'w+') as f:
    f.write('')


def load_KB():
    global nlp
    '''Ricordarsi di mettere la kb più grossa'''
    nlp = en_core_web_sm.load()


# Caqricamento JSON con le pozioni
def load_json():
    global pozioni
    with open('pozioni.json') as json_file:
        pozioni = json.load(json_file)


'''
    Funzioni Utility
'''


# serve per creare l'immagine del parsing
def displayParser(frase):
    global imageCounter
    svg = displacy.render(frase, style="dep")
    output_path = Path("result_spacy.svg")
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
    return dict


# serve per parsificare le entity e vedere se nella frase c'è un nome proprio di persona
def parser_ne(frase):
    list_name = ["Enrico", "Alberto", "Alessandro"]
    for name in list_name:
        if name.lower() in frase.lower():
            return name

    frase_parsata = nlp(frase)
    dict = {}
    for token in frase_parsata.ents:
        dict[token.text] = [token.text, token.start_char, token.end_char, token.label_]
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
def selectPoison(difficolta):
    while True:
        pozionicopia = pozioni
        pozione = random.choice(list(pozionicopia))
        if pozionicopia[pozione][0] == difficolta:
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


def checkScream(frase):
    if frase.isupper():
        print("\nDon't scream!\n")
        sleep(2)


def checkQuestion(frase):
    if "?" in frase:
        print("I'm asking the questions, not you!\n")
        sleep(2)


def checkFrase(frase):
    checkScream(frase)
    checkQuestion(frase)


def write_question(question):
    with open('memory/questions.txt', 'rb') as f:
        qst_list = pickle.load(f)

    with open('memory/questions.txt', 'wb') as f:
        # aggiungo la domanda alla lista
        if not qst_list:
            qst_list = [question]
        else:
            qst_list.append(question)

        pickle.dump(qst_list, f)


def repeat_question():
    with open('memory/questions.txt', 'rb') as f:
        qst_list = pickle.load(f)
    return str(qst_list[-1])


def write_answer(answer, score):
    with open('memory/answers.txt', 'a+') as f:
        score = str(score)

        if score == 'separator':
            f.write(answer)
        elif 'sbagliata' in score:
            f.write(answer + ' ' + score)
        else:
            f.write(answer + ' - score: ' + score)
        f.write('\n')


def ask_question(pozione, domande_fatte, ingredienti_pozione, ingredienti_indovinati, difficolta, domande_pozione,
                 aiuto):
    # per la memoria
    if domande_pozione == 0 and domande_fatte >= 1:
        write_answer('\n--------------------------\n', 'separator')

    # faccio la domanda
    if not aiuto:
        if domande_fatte == 0:
            risposta = input(
                sp.printAskPotion(pozione, ingredienti_pozione, domande_fatte, domande_pozione))
        else:
            risposta = input(sp.printAskPotion(pozione, ingredienti_pozione, domande_fatte, domande_pozione))

    # aiuto lo studente con una domanda vero/falso
    else:
        ingrediente = random.choice(get_all_ingredients())

        risposta_giusta = 'no'
        if ingrediente in [ingr.lower() for ingr in ingredienti_pozione]:
            risposta_giusta = 'yes'

        risposta = str(input(ingrediente + ' is an ingredient of ' + pozione + '?\n')).lower()

        while 'again' in risposta.lower() or 'repeat' in risposta.lower() or 'what?' in risposta.lower():
            risposta = input(repeat_question()).lower()

        else:
            if risposta == risposta_giusta:
                print('Correct')

                score = difficolta * len(ingrediente.split()) / 2
                write_answer(risposta, score)

                return ingredienti_pozione, domande_pozione + 1, float(score)

            # risposta sbagliata, ma rispondo sensato
            elif risposta == 'yes' or risposta == 'no' or 'don\'t know' in risposta:
                if 'don\'t know' in risposta.lower():
                    print('-Don\'t know- it\'s not in my vocabulary!')
                else:
                    wrong_ingredient()
                score = float(-(difficolta * len(ingrediente.split()) / 3))
                write_answer(risposta, score)

                return ingredienti_pozione, domande_pozione + 2, score

            # tutte le altre risposte
            else:
                print('You must answer to me with valid answer!')
                score = float(-20)
                write_answer(risposta, score)

                return ingredienti_pozione, domande_pozione + 2, score

    # controlla la risposta e analizzo l'ingrediente
    while 'again' in risposta.lower() or 'repeat' in risposta.lower() or 'what?' in risposta.lower():
        risposta = input(repeat_question())

    if 'don\'t know' in risposta.lower():
        # salta alla domanda successiva
        score = float(-(difficolta * len(ingredienti_pozione) * 2))
        write_answer(risposta, score)
        ingredienti_pozione = []

        print(ingredienti_pozione)

        return ingredienti_pozione, len(ingredienti_pozione) + 1, score

    if 'ingredient' in risposta:

        risposta_completa = risposta

        # necessario in quanto spacy non li classifica come attr
        if 'lavender' in risposta:
            risposta = 'lavender'
        elif 'mint' in risposta:
            risposta = 'mint'
        else:
            risposta = str(get_ingredient(risposta, False))

        ingredienti_pozione, is_correct = check_ingredient(risposta, ingredienti_pozione)

        if risposta in ingredienti_indovinati:
            score = -10.0
            write_answer(risposta + " -> ingrediente ripetuto - score: " + str(score), "separator")
            print("Correct, but you have already guessed this ingredient!\n")
            return ingredienti_pozione, domande_pozione + 1, score

        if is_correct:
            score = difficolta * len(risposta.split())
            write_answer(risposta_completa, score)
            ingredienti_indovinati.append(risposta)

            return ingredienti_pozione, domande_pozione + 1, score
        else:
            wrong_ingredient()
            write_answer(risposta, 'sbagliata -> aiuto')
            return ask_question(pozione, domande_fatte, ingredienti_pozione, ingredienti_indovinati, difficolta,
                                domande_pozione, True)

    else:
        if risposta in ingredienti_indovinati:
            score = -10.0
            write_answer(risposta + " -> ingrediente ripetuto - score: " + str(score), "separator")
            print("Correct, but you have already guessed this ingredient!\n")
            return ingredienti_pozione, domande_pozione + 1, score

        if risposta in ingredienti_pozione:
            ingredienti_pozione.remove(risposta)
            ingredienti_indovinati.append(risposta)

            score = difficolta * len(risposta.split())
            write_answer(risposta, score)

            return ingredienti_pozione, domande_pozione + 1, score
        else:
            wrong_ingredient()
            write_answer(risposta, 'sbagliata -> aiuto')

            return ask_question(pozione, domande_fatte, ingredienti_pozione, ingredienti_indovinati, difficolta,
                                domande_pozione, True)


'''
    SPACY
'''


def get_ingredient(frase, aiuto):
    if aiuto:
        return
    sent_dict = {}
    frase_parsificata = nlp(frase)
    displayParser(frase_parsificata)

    position = 'nsubj'

    for chunk in frase_parsificata.noun_chunks:
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
        'Is this Avanti un Altro?! I\'m not Paolo Bonolis!\n',
        'Good answer... but it\'s wrong!\n',
        'That\'s a pity, try again\n'
    ]
    print(random.choice(sentences))
    return


def check_ingredient(ingrediente, ingredienti):
    print(ingrediente, ingredienti)
    if ingrediente in ingredienti:
        print("Correct!\n")
        sp.printAskIngredient(len(ingredienti))
        ingredienti.remove(ingrediente)
        return ingredienti, True
    else:
        return ingredienti, False


# funzione per timeout attesa input
def answer_casata(casata_nome):
    casata_nome =  casata_nome.lower()
    if casata_nome == "gryffindor" or casata_nome == "hufflepuff" or casata_nome == "ravenclaw" or casata_nome == "slytherin":
        print("\n" + "Ok let's proceed!")
        return casata_nome
    else:
        print("You must tell me a valid house name!")
        casata_nome = input("\n" + sp.ask_info("house") + "\n")
        return answer_casata(casata_nome)
