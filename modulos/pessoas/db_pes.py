import pickle

#chatgpt

def carregar_pessoas():
    try:
        with open('DataBase/pessoas.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {'clientes': {}, 'vendedores': {}}

def salvar_pessoas(pessoas):
    with open('DataBase/pessoas.pkl', 'wb') as file:
        pickle.dump(pessoas, file)