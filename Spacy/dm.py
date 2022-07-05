import csv

dict_pozioni = {
    'oculare': {
        'numero_ingr': 4,
        'ingredienti': ['assenzio',
                        'mandragora umido',
                        'corno unicorno',
                        'polvere blu identificata']},
    'pompion': {
        'numero_ingr': 1,
        'ingredienti': ['flitterby',
                        'bulbo rimbalzante',
                        'digitale']},
    'obliviosa': {
        'numero_ingr': 4,
        'ingredienti': ['acqua fiume lete',
                        'bacche vischio',
                        'radici valeriana',
                        'ingrediente Base']},
    'erbicida': {
        'numero_ingr': 4,
        'ingredienti': ['spine pesce-leone',
                        'muco flobber',
                        'succo horklump',
                        'ingrediente base']},
    'aguzzaingegno': {
        'numero_ingr': 4,
        'ingredienti': ['milza tritone',
                        'uova runespoor',
                        'scarabei',
                        'radici zenzero',
                        'bile armadillo']},
}
ingredienti_trovati = []


def check_trovati(pozione):

    if len(ingredienti_trovati) == dict_pozioni[pozione]['numero_ingr']:
        return True
    else:
        return False


def check_ingrediente(pozione, ingrediente):
    if ingrediente.lower() in dict_pozioni[pozione]['ingredienti']:
        if ingrediente in ingredienti_trovati:
            print('Hai già detto questo ingrediente!')
        else:
            print('Ingrediente corretto')
            ingredienti_trovati.append(ingrediente)
    else:
        print('Sicuro %s sia un ingrediente di %s?' % (ingrediente, pozione))

    if check_trovati(pozione):
        print('ok')
        return 'ok'


if __name__ == '__main__':
    pozione = 'pompion'
    ingrediente = 'flitterby'
    check_ingrediente(pozione, ingrediente)