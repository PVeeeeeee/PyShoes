import os
import re
from datetime import datetime

from pytz import timezone
from tabulate import tabulate

import modulos.pessoas.db_pes as db_pes
import modulos.pessoas.menu_pes as menu_pes
import modulos.vendas.db_ven as db_ven


#funcoes 1 e 2 feitas pelo chatgpt
def verificar_nome(nome):
    padrao = re.compile(r'^[a-zA-Z\s]+$')

    return bool(padrao.match(nome))

def validar_cpf(cpf):
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = 11 - (soma % 11)
    dv1 = resto if resto < 10 else 0
    if dv1 != int(cpf[9]):
        return False
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = 11 - (soma % 11)
    dv2 = resto if resto < 10 else 0
    if dv2 != int(cpf[10]):
        return False
    return True

#ajustar 
def verificar_telefone(telefone):
    telefone = telefone.strip()
    
    return bool(telefone.isdigit() and len(telefone) >= 9 and len(telefone) <= 13)


def verificar_existencia(cpf, type):
    if type == "c":   
        pessoas = db_pes.carregar_pessoas()
        return cpf in pessoas['clientes']
    elif type == "v":
        pessoas = db_pes.carregar_pessoas()
        return cpf in pessoas['vendedores']



def buscar_pessoa(cpf):
    try:
        pessoas = db_pes.carregar_pessoas()
    
        if cpf in pessoas['clientes']:
            print('Pessoa encontrada:')
            print(tabulate(pessoas['clientes'][cpf].items(), tablefmt="pretty"))
        if cpf in pessoas['vendedores']:
                print(tabulate(pessoas['vendedores'][cpf].items(), tablefmt="pretty"))

        while True:
            sub_menu = input("\nO que você quer fazer?\n1- Editar pessoa\n2- Deletar pessoa\n0- Voltar\n")

            if sub_menu == "1":
                editar_pes(cpf)
                
            elif sub_menu == "2":
                if cpf in pessoas['clientes'] and cpf in pessoas['vendedores']:
                    sub_menu2 = input("Deseja deletar apenas Vendedor ou os 2 cadastros?\n1- Apenas Vendedor\n2- Cliente e Vendedor\n0- Voltar\n")
                    if sub_menu2 == "1":
                        deletar_pes(cpf, "v")
                    elif sub_menu2 == "2":
                        deletar_pes(cpf, "dupla")
                    elif sub_menu2 == "0":
                        os.system("clear")
                        return menu_pes.main()
                    else:
                        print("Opção inválida")
                        
                else:
                    deletar_pes(cpf, "c")
                    
            elif sub_menu == "0":
                os.system('clear')
                return menu_pes.main()
            else:
                print("Opção inválida")

    except Exception as e:
        print(f"Erro ao buscar pessoa: {e}")



def editar_pes(cpf):
    try:
        pessoas = db_pes.carregar_pessoas()

        vendedor = pessoas['vendedores'].get(cpf, None)
        cliente = pessoas['clientes'].get(cpf, None)

        print("Editar pessoa:")

        while True:
            novo_nome = input("Novo nome: ")
            if novo_nome.strip() == "0":
                os.system("clear")
                return menu_pes.main()
            if novo_nome:
                if verificar_nome(novo_nome):
                    if vendedor:
                        vendedor["nome"] = novo_nome
                    if cliente:
                        cliente["nome"] = novo_nome
                    break
                else:
                    print("Nome Inválido")
            else:
                break

        while True:
            novo_telefone = input("Novo Telefone: ").strip()
            if novo_telefone.strip() == "0":
                os.system("clear")
                return menu_pes.main()
            if novo_telefone:
                if verificar_telefone(novo_telefone):
                    if vendedor:
                        vendedor['telefone'] = novo_telefone
                    if cliente:
                        cliente['telefone'] = novo_telefone
                    break
                else:
                    print("Telefone inválido.")
            else:
                break
                    
        db_pes.salvar_pessoas(pessoas)
        os.system("clear")

        
        vendas = db_ven.carregar_vendas()

        if novo_nome or novo_telefone:
            for venda in vendas:
                if vendedor:
                    if venda['cpf_vendedor'] == vendedor['cpf']:
                        venda["data_edit"] = datetime.now(timezone('America/Sao_Paulo')).strftime("%d/%m/%y %H:%M")
                if cliente:
                    if venda['cpf_cliente'] == cliente['cpf']:
                        venda["data_edit"] = datetime.now(timezone('America/Sao_Paulo')).strftime("%d/%m/%y %H:%M")
            db_ven.salvar_vendas(vendas)
            
        os.system("clear")
        print("Pessoa editada com sucesso!")
        buscar_pessoa(cpf)

    except Exception as e:
        print(f"Erro ao editar pessoa: {e}")



def deletar_pes(cpf, condicao):
    try:
        pessoas = db_pes.carregar_pessoas()
        cliente = pessoas['clientes']
        vendedor = pessoas['vendedores']

        os.system("clear")

        if condicao == "dupla":
            del cliente[cpf]
            del vendedor[cpf]
            print("Pessoa deletada com sucesso!")
        elif condicao == "v":
            del vendedor[cpf]
            print("Vendedor deletado com sucesso!")
        elif condicao == "c":
            del cliente[cpf]
            print("Cliente deletado com sucesso!")
        db_pes.salvar_pessoas(pessoas)
        return menu_pes.main()
        
    except Exception as e:
        print(f"Erro ao deletar pessoa: {e}")