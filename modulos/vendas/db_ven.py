import pickle

#chatgpt

def carregar_vendas():
    try:
        with open('DataBase/vendas.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

def salvar_vendas(vendas):
    with open('DataBase/vendas.pkl', 'wb') as file:
        pickle.dump(vendas, file)