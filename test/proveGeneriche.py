import spacy
from pathlib import Path
from spacy import displacy
import it_core_news_lg

imageCounter=0
nlp = it_core_news_lg.load()


def parser_ne(frase):
    frase_parsata=nlp(frase)
    dict = {}
    for token in frase_parsata.ents:
        dict[token.text]=[token.text, token.start_char, token.end_char, token.label_]
        #print(f"text={token.text},inizio_stringa={token.start_char}, fine_stringa={token.end_char}, etichetta={token.label_}")
    for key, value in dict.items():
        if("PER" in value):
            return key
    return None


risposta_nome = "mi chiamo Alessio"
nome=parser_ne(risposta_nome)
nome
if(nome is not None):
    print(f"Ciao, {nome}")
