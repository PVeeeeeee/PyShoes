import os

import modulos.main.menu_principal as menu_principal
import modulos.pessoas.db_pes as db_pes
import modulos.pessoas.funcoes_cli as funcoes_cli
import modulos.pessoas.funcoes_fun as funcoes_fun
import modulos.pessoas.funcoes_pes as funcoes_pes


def main():
    while True:
        menu = input(''':::::::PESSOAS:::::::
        
1- Adicionar Cliente
2- Adicionar Vendedor 
3- Checar pessoa
4- Relatórios
0- Menu Principal
''').strip()

        if menu == "1":
            try:

                while True:
                    cpf = input("CPF do cliente: ").strip()
                    if cpf == "0":
                        break
                    elif not funcoes_pes.validar_cpf(cpf):
                        print("CPF inválido. Por favor, insira um CPF válido.")
    
                    elif funcoes_pes.verificar_existencia(cpf, "c"):
                        print("CPF já está em uso. Por favor, insira um CPF válido.")
    
                    else:
                        break
                if cpf == "0":
                    os.system("clear")
                    continue
                    
                while True:
                    nome = input("Nome do cliente: ")
                    if nome =="0":
                        break
                    elif not funcoes_pes.verificar_nome(nome):
                        print("Nome Inválido")
                    else:
                        break
    
                if nome =="0":
                    os.system('clear')
                    continue
    
                while True:
                    telefone = input("telefone: ").strip()
                    if telefone == "0":
                        break
                    elif not funcoes_pes.verificar_telefone(telefone):
                        print("Telefone Inválido")
                    else:
                        break
    
                if telefone =="0":
                    os.system('clear')
                    continue
                    
                funcoes_cli.adicionar_cli(nome, cpf, telefone)
            except Exception as e:
                print(f"Erro ao enviar dados do cliente: {e}")

        elif menu == "2":
            try:
                while True:
                    cpf = input("CPF do vendedor: ").strip()
                    if cpf == "0":
                        break
                    elif not funcoes_pes.validar_cpf(cpf):
                        print("CPF inválido. Por favor, insira um CPF válido.")
                    elif funcoes_pes.verificar_existencia(cpf, "v"):
                        print("CPF de vendedor já está em uso. Por favor, insira um CPF válido.")
                    
                    elif funcoes_pes.verificar_existencia(cpf, "c"):
                        pessoas = db_pes.carregar_pessoas()
                        nome = pessoas["clientes"][cpf]["nome"]
                        telefone = pessoas["clientes"][cpf]["telefone"]
                        funcoes_fun.adicionar_fun(nome, cpf, telefone)
    
                    else:
                        while True:
                            nome = input("Nome do vendedor: ")
                            if nome =="0":
                                break
                            elif not funcoes_pes.verificar_nome(nome):
                                print("Nome Inválido")
                            else:
                                break
                        
                        if nome =="0":
                            os.system('clear')
                            continue
    
                        while True:
                            telefone = input("telefone: ").strip()
                            if telefone == "0":
                                break
                            elif not funcoes_pes.verificar_telefone(telefone):
                                print("Telefone Inválido")
                            else:
                                funcoes_fun.adicionar_fun(nome, cpf, telefone, "dupla")
                                funcoes_cli.adicionar_cli(nome, cpf, telefone, "dupla")
    
                        if telefone =="0":
                            os.system('clear')
                            continue
                            
                if cpf == "0":
                    os.system('clear')
                    continue
                    
            except Exception as e:
                print(f"Erro ao enviar dados do vendedor: {e}")


        elif menu == "3":
            while True:
                cpf = input("Insira o CPF: ").strip()
                if cpf == "0":
                    break
                elif not funcoes_pes.validar_cpf(cpf):
                    print("CPF inválido. Por favor, insira um CPF válido.")
                elif not funcoes_pes.verificar_existencia(cpf, "c") and not funcoes_pes.verificar_existencia(cpf, "v"):
                    print("Pessoa não encontrada (0 p/ cancelar busca\n")
                else:
                    os.system("clear")
                    funcoes_pes.buscar_pessoa(cpf)

            if cpf == "0":
                os.system('clear')
                continue
                
        elif menu =="4":
            while True:
                os.system("clear")
                submenu = input('''Qual Relatório quer acessar?
                
1- Clientes
2- Vendedores
0- Voltor
''')
                if submenu == "0":
                    os.system("clear")
                    break
                elif submenu == "1":
                    funcoes_cli.relatorio_cli()
                elif submenu == "2":
                    funcoes_fun.relatorio_fun()
                else:
                    os.system("clear")
                    print("Opção Inválida")
                break
                

        elif menu == "0":
            os.system('clear')
            menu_principal.main()

        else:
            os.system('clear')
            print("\nX Opção inválida X\n")