import os
import pickle


def carregar_produtos():
    if os.path.exists("DataBase/produtos.pkl"):
        with open("DataBase/produtos.pkl", "rb") as file:
            return pickle.load(file)
    else:
        return []


def salvar_produtos(produtos):
    with open("DataBase/produtos.pkl", "wb") as file:
        pickle.dump(produtos, file)
