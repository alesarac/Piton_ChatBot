import spacy
from pathlib import Path
from spacy import displacy
import time

nlp = spacy.load("it_core_news_md")

ingredientePozione = "acqua"

def displayParser(frase):
    svg = displacy.render(frase, style="dep")
    output_path = Path("./images/dependency_plot.svg")
    output_path.open("w", encoding="utf-8").write(svg)

def parser(fraseIngrediente):
    dict = {}
    print(fraseIngrediente)
    for token in fraseIngrediente:
        dict[token.text]=[token.dep_,token.head.text,token.head.pos_,[child for child in token.children]]
        print(f"text={token.text},dep={token.dep_}, head_text={token.head.text},figli={[child for child in token.children]}")
    print("\n\n")
    displayParser(nlp(fraseIngrediente))
    return dict

#frasi prova
frase1="l'acqua è un ingrediente"
frase2="un'ingrediente è l'acqua"
frase3="un'ingrediente per fare la pasta è l'acqua"
frase4="l'acqua è un'ingrediente per fare la pasta"
frase5="un'ingrediente è l'acqua, per fare la pasta"

#frase che senza la virgola fotterebbe il sistema
frase6="per fare la pasta, un'ingrediente è l'acqua"


dict = parser(nlp(frase1))
dict = parser(nlp(frase2))
dict = parser(nlp(frase3))
dict = parser(nlp(frase4))
dict = parser(nlp(frase5))
dict = parser(nlp(frase6))

