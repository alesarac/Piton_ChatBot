from pathlib import Path
import spacy
from spacy import displacy

# caricare la KB allenata in italiano "python -m spacy download it_core_news_md"
nlp = spacy.load("en_core_web_sm")
imageCounter = 0
ingredientePozione = "Criniera di Granian"


def displayParser(frase):
    global imageCounter
    imageCounter = imageCounter + 1
    svg = displacy.render(frase, style="dep")
    output_path = Path("./images/dependency_plot{0}.svg".format(imageCounter))
    output_path.open("w", encoding="utf-8").write(svg)


# serve per parsificare le dipendenze, la head.text, e i figli  di una frase data in input
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


ciao = parser_dep("yes,i studied all day")
print(ciao)
