import os
from datetime import datetime

from pytz import timezone
from tabulate import tabulate

import modulos.pessoas.db_pes as db_pes
import modulos.pessoas.menu_pes as menu_pes
import modulos.vendas.db_ven as db_ven


def adicionar_cli(nome, cpf, telefone, condicao=None):
    try:
        pessoas = db_pes.carregar_pessoas()
        
        cliente = {
            'nome': nome,
            'cpf': cpf,
            'telefone': telefone,
            'funcao': "Cliente",
            'data_de_cadastro': datetime.now(timezone('America/Sao_Paulo')).strftime("%d/%m/%y %H:%M"),
            'produtos_comprados': "R$ 0.0",
        }
        
        pessoas['clientes'][cpf] = cliente
        db_pes.salvar_pessoas(pessoas)
        
        if condicao == "dupla":
            print("Cliente adicionado automaticamente!")
            return menu_pes.main()
        elif condicao == "pass":
            print("Cliente adicionado com sucesso!")
            return
        else:
            os.system("clear")
            print("Cliente adicionado com sucesso!")
            return menu_pes.main()
            
    except Exception as e:
        print(f"Erro ao adicionar cliente: {e}")



def calcular_prodcom():
    try:
        vendas = db_ven.carregar_vendas()
        pessoas = db_pes.carregar_pessoas()

        clientes = pessoas['clientes']
        valor_total = 0

        for cliente in clientes.values():
            cliente['produtos_comprados'] = 0

        for venda in vendas:
            cpf_cliente = venda['cpf_cliente']
            valor_venda = venda['valor']

            if cpf_cliente in clientes:
                valor_total += valor_venda
                clientes[cpf_cliente]['produtos_comprados'] = f"R$ {valor_total:.2f}"

        db_pes.salvar_pessoas(pessoas)

    except Exception as e:
        print(f"Erro ao atualizar produtos vendidos dos clientes: {e}")




#molde da tabela feito pelo chatgpt

def relatorio_cli():
    try:
        pessoas = db_pes.carregar_pessoas()

        clientes = sorted(pessoas['clientes'].items(), key=lambda x: x[1]['nome'])

        if clientes:

            headers = [
                "Nome", "CPF", "Telefone", "Função", "Data de Cadastro",
                "Produtos Comprados", "Nível Cliente"
            ]

            clientes_tabela = [[
                dados['nome'], dados['cpf'], dados['telefone'], dados['funcao'],
                dados['data_de_cadastro'], dados['produtos_comprados']
            ] for cpf, dados in clientes]

            clientes_tabela.insert(0, headers)

            os.system("clear")
            print(tabulate(clientes_tabela, headers="firstrow", tablefmt="pretty"))
            submenu = input("0- voltar\n")
            if submenu == "0":
                os.system("clear")
                return
            else:
                os.system("clear")
                print("Opção Inválida")
                return

        else:
            os.system("clear")
            print("Nenhum cliente encontrado.")

    except Exception as e:
        print(f"Erro ao exibir relatorio dos clientes: {e}")
