from tabulate import tabulate

import modulos.pessoas.db_pes as db_pes
import modulos.pessoas.funcoes_cli as funcoes_cli
import modulos.pessoas.funcoes_fun as funcoes_fun


def verificar_existencia(cpf):
    pessoas = db_pes.carregar_pessoas()
    return cpf in pessoas['vendedores'] or cpf in pessoas['clientes']



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
    

def buscar_pessoa(cpf):
    try:
        pessoas = db_pes.carregar_pessoas()
        if cpf in pessoas['vendedores']:
            tipo = "vendedor"
            print("Vendedor encontrado:")
            print(tabulate(pessoas['vendedores'][cpf].items(), tablefmt="pretty"))
        elif cpf in pessoas['clientes']:
            tipo = "clitente"
            print("Cliente encontrado:")
            print(tabulate(pessoas['clientes'][cpf].items(), tablefmt="pretty"))
        else:
            print("Pessoa não encontrada.")
            return
    
        sub_menu = input(f"\nO que você quer fazer?\n1- Editar {tipo}\n2- Deletar {tipo}\n0- Voltar\n")

        
        
        if sub_menu == "1":
            if cpf in pessoas['clientes']:
                funcoes_cli.editar_cli(cpf)
            elif cpf in pessoas['vendedores']:
                funcoes_fun.editar_ven(cpf)
        elif sub_menu == "2":
            deletar_pes(cpf)
        elif sub_menu == "0":
            return
        else:
            print("Opção inválida")
            
    except Exception as e:
        print(f"Erro ao buscar pessoa: {e}")


def deletar_pes(cpf):
    pessoas = db_pes.carregar_pessoas()
    try:
        if cpf in pessoas['vendedores']:
            del pessoas['vendedores'][cpf]
        elif cpf in pessoas['clientes']:
            del pessoas['clientes'][cpf]

        db_pes.salvar_pessoas(pessoas)
        print("pessoa deletada com sucesso!")
    except Exception as e:
        print(f"Erro ao deletar pessoa: {e}")


