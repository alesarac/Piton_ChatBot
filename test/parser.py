import utilities as util

util.load_KB()
domande = 2
domande_fatte = 0

ingredienti_indovinati = []
all_ingredienti = util.get_all_ingredients()
score = 0
pozioneScelta_dict = util.selectPoison(2)
nome_pozione = str(list(pozioneScelta_dict.keys())[0])
ingredienti_pozione = list(pozioneScelta_dict.values())[0][1]
domande_pozione = len(ingredienti_pozione) + 1

print(util.ask_question(nome_pozione, domande_fatte, ingredienti_pozione,
                        ingredienti_indovinati, 2,
                        False, False))
