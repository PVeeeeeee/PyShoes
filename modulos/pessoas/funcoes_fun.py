from datetime import datetime

from pytz import timezone

import modulos.pessoas.db_pes as db_pes
import modulos.pessoas.funcoes_pes as funcoes_pes
import modulos.vendas.db_ven as db_ven

data_now = datetime.now(timezone('America/Sao_Paulo'))

def adicionar_ven(nome, cpf):
    try:
        pessoas = db_pes.carregar_pessoas()
        vendedor = {
            'nome': nome,
            'cpf': cpf,
            'funcao': "Vendedor",
            'data_de_cadastro': data_now.strftime("%d/%m/%Y %H:%M"),
            'produtos_vendidos': 0,
            'comissao' : 0
        }
        pessoas['vendedores'][cpf] = vendedor
        db_pes.salvar_pessoas(pessoas)
        print("Vendedor adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar vendedor: {e}")


def editar_ven(cpf):
    pessoas = db_pes.carregar_pessoas()
    try:
        vendedor = pessoas['vendedores'][cpf]
        print("Editar vendedor:")

        vendedor["nome"] = input("Novo nome: ") or vendedor["nome"]

        while True:
            novo_cpf = input("Novo CPF: ")
            if novo_cpf:
                if funcoes_pes.validar_cpf(novo_cpf):
                    if not funcoes_pes.verificar_existencia(novo_cpf):
                        vendedor['cpf'] = novo_cpf
                        break
                    else:
                        print("CPF já cadastrado.")
                else:
                    print("CPF inválido.")
            else:
                break
        db_pes.salvar_pessoas(pessoas)
        print("Vendedor editado com sucesso!")
    except Exception as e:
        print(f"Erro ao editar vendedor: {e}")



def calcular_comissao():
    try:
        vendas = db_ven.carregar_vendas()
        pessoas = db_pes.carregar_pessoas()

        vendedores = pessoas['vendedores']

        if data_now.day == 1 or not vendas:
            for vendedor in vendedores.values():
                vendedor["comissao"] = 0

        for vendedor in vendedores.values():
            comissao_total = 0

            for venda in vendas:
                data_venda = datetime.strptime(venda["data_venda"], '%d/%m/%y %H:%M')
                if data_venda.month == data_now.month and data_venda.year == data_now.year:
                    comissao_total += venda["valor"]
        
            vendedor["comissao"] = round((comissao_total * 0.05), 2)

        db_pes.salvar_pessoas(pessoas)

    except Exception as e:
        print(f"Erro ao calcular comissões mensais: {e}")
