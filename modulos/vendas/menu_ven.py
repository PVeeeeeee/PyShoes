import os

import modulos.main.menu_principal as menu_principal
import modulos.pessoas.db_pes as db_pes
import modulos.pessoas.funcoes_pes as funcoes_pes
import modulos.produtos.db_pro as db_pro
import modulos.vendas.funcoes_ven as funcoes_ven


def main():
    while True:
        menu = input('''::::::VENDAS::::::

1- Vender Produto
2- Checar Vendas
3- Relatório
0- Menu Principal

''').strip()

        if menu == "1":
            try:
                produtos = db_pro.carregar_produtos()
                pessoas = db_pes.carregar_pessoas()

                while True:
                    codigo = input("Insira o código do produto: ")
                    if codigo == "0":
                        os.system("clear")
                        break
                    produtos_encontrados = [
                        prod for prod in produtos if int(prod["codigo"]) == int(codigo) and prod['marcador'] != "deleted"
                    ]

                    if produtos_encontrados:
                        break
                    else:
                        print(f"Nunhum produto com o código {codigo} foi encontrado (0 p/ Voltar)")

                if codigo == "0":
                    continue

                while True:
                    cpf_cliente = input("Insira o CPF do cliente: ")
                    if cpf_cliente == "0":
                        os.system("clear")
                        break

                    if not funcoes_pes.validar_cpf(cpf_cliente):
                        print("Por favor, insira um CPF válido.")

                    elif cpf_cliente not in pessoas['clientes']:
                        funcoes_ven.cria_cliente(cpf_cliente)
                        break
                    else:
                        break

                if cpf_cliente == "0":
                    continue

                while True:
                    cpf_vendedor = input("Insira o CPF do vendedor: ")
                    if cpf_vendedor == "0":
                        os.system("clear")
                        break

                    if not funcoes_pes.validar_cpf(cpf_vendedor):
                        print("Por favor, insira um CPF válido.")

                    elif cpf_vendedor not in pessoas['vendedores']:
                        print(f"Vendedor com CPF {cpf_vendedor} não encontrado.")
                    else:
                        break

                if cpf_vendedor == "0":
                    continue

                funcoes_ven.vender_produto(codigo, cpf_cliente, cpf_vendedor)

            except Exception as e:
                print(f"Ocorreu um erro inesperado: {e}")

        elif menu == "2":
            try:
                dado_de_busca = input("Insira o código do produto ou CPF do cliente/vendedor: ")
                if dado_de_busca == "0":
                    os.system("clear")
                    continue

                if funcoes_pes.validar_cpf(dado_de_busca):
                    os.system("clear")
                    funcoes_ven.buscar_venda(cpf=dado_de_busca)
                else:
                    os.system("clear")
                    funcoes_ven.buscar_venda(codigo=dado_de_busca)

            except Exception as e:
                print(f"Ocorreu um erro inesperado: {e}")

        elif menu == "3":
            os.system("clear")
            funcoes_ven.relatorio_ven()

        elif menu == "0":
            os.system('clear')
            menu_principal.main()

        else:
            os.system('clear')
            print("\nX Opção inválida X\n")