import pickle

#chatgpt

def carregar_produtos():
    try:
        with open("DataBase/produtos.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

def salvar_produtos(produtos):
    with open("DataBase/produtos.pkl", "wb") as file:
        pickle.dump(produtos, file)