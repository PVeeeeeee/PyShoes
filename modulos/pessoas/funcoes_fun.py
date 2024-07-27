import os
from datetime import datetime

import pytz
from pytz import timezone
from tabulate import tabulate

import modulos.pessoas.db_pes as db_pes
import modulos.pessoas.menu_pes as menu_pes
import modulos.vendas.db_ven as db_ven
    

def adicionar_fun(nome, cpf, telefone, condicao=None):
    try:
        pessoas = db_pes.carregar_pessoas()
        
        vendedor = {
            'nome': nome,
            'cpf': cpf,
            'telefone': telefone,
            'funcao': "Vendedor",
            'data_de_cadastro': datetime.now(timezone('America/Sao_Paulo')).strftime("%d/%m/%y %H:%M"),
            'produtos_vendidos': "R$ 0.0",
            'comissao' : "R$ 0.0"
        }
        
        pessoas['vendedores'][cpf] = vendedor
        db_pes.salvar_pessoas(pessoas)
        
        os.system("clear")
        if condicao == "dupla":
            print("Vendedor adicionado com sucesso!")     
        else:
            print("CPF já pertence a um Cliente, vendedor será criado automaticamente\n")
            print("Vendedor adicionado com sucesso!")
            return menu_pes.main()
            
    except Exception as e:
        print(f"Erro ao adicionar vendedor: {e}")



def calcular_prodven():
    try:
        vendas = db_ven.carregar_vendas()
        pessoas = db_pes.carregar_pessoas()

        vendedores = pessoas['vendedores']
        valor_total = 0

        for vendedor in vendedores.values():
            vendedor['produtos_vendidos'] = 0

        for venda in vendas:
            cpf_vendedor = venda['cpf_vendedor']
            valor_venda = venda['valor']

            if cpf_vendedor in vendedores:
                valor_total += valor_venda
                vendedores[cpf_vendedor]['produtos_vendidos'] = f"R$ {valor_total:.2f}"

        db_pes.salvar_pessoas(pessoas)

    except Exception as e:
        print(f"Erro ao atualizar produtos vendidos: {e}")

#feito com auxílio do ChatGPT

def calcular_comissao():
    try:
        data_now = datetime.now(pytz.timezone('America/Sao_Paulo'))

        vendas = db_ven.carregar_vendas()
        pessoas = db_pes.carregar_pessoas()

        vendedores = pessoas['vendedores']

        for vendedor in vendedores.values():
            comissao_total = 0

            vendas_do_fun = [venda for venda in vendas if venda['cpf_vendedor'] == vendedor['cpf']]

            for venda in vendas_do_fun:
                data_venda = datetime.strptime(venda["data_venda"], '%d/%m/%y %H:%M').replace(tzinfo=pytz.timezone('America/Sao_Paulo'))

                if data_venda.month == data_now.month and data_venda.year == data_now.year:
                    comissao_total += venda["valor"]

            vendedor["comissao"] = f"R$ {round(comissao_total * 0.03, 2):.2f}"

        db_pes.salvar_pessoas(pessoas)

    except Exception as e:
        print(f"Erro ao calcular comissões mensais: {e}")


#molde da tabela feito pelo chatgpt

def relatorio_fun():
    try:
        pessoas = db_pes.carregar_pessoas()

        vendedores = sorted(pessoas['vendedores'].items(), key=lambda x: x[1]['nome'])

        if vendedores:
            headers = ["Nome", "CPF", "Telefone", "Função", "Data de Cadastro", "Produtos Vendidos", "Comissão"]

            vendedores_tabela = [[dados['nome'], dados['cpf'], dados['telefone'], dados['funcao'], dados['data_de_cadastro'], dados['produtos_vendidos'], dados['comissao']] for cpf, dados in vendedores]

            vendedores_tabela.insert(0, headers)

            os.system("clear")
            print(tabulate(vendedores_tabela, headers="firstrow", tablefmt="pretty"))
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
            print("Nenhum vendedor encontrado.")

    except Exception as e:
        print(f"Erro ao exibir relatório dos vendedores: {e}")