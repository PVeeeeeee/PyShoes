import pickle


def carregar_pessoas():
    try:
        with open('modulos/pessoas/pessoas.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {'clientes': {}, 'vendedores': {}}

def salvar_pessoas(pessoas):
    with open('modulos/pessoas/pessoas.pkl', 'wb') as file:
        pickle.dump(pessoas, file)