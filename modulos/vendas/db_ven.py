import pickle


def carregar_vendas():
    try:
        with open('modulos/vendas/vendas.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

def salvar_vendas(vendas):
    with open('modulos/vendas/vendas.pkl', 'wb') as file:
        pickle.dump(vendas, file)

def registrar_venda(venda):
    vendas = carregar_vendas()
    vendas.append(venda)
    salvar_vendas(vendas)
    print("Venda registrada com sucesso!")
