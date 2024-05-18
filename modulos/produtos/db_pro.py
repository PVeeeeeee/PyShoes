import os
import pickle


def carregar_produtos():
    if os.path.exists("modulos/produtos/produtos.pkl"):
        with open("modulos/produtos/produtos.pkl", "rb") as file:
            return pickle.load(file)
    else:
        return []


def salvar_produtos(produtos):
    with open("modulos/produtos/produtos.pkl", "wb") as file:
        pickle.dump(produtos, file)
