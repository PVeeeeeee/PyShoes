import os

import modulos.main.menu_principal as menu_principal
import modulos.produtos.db_pro as db_pro
import modulos.produtos.funcoes_pro as funcoes_pro


def main():
    while True:
        menu = input(''':::::::::PRODUTOS:::::::::
        
1- Adicionar novo produto
2- Checar Produto
3- Relatório 
0- Menu Principal

''').strip()
        
        if menu == "1":

            while True:
                try:
                    codigo = int(input("Código do produto: ").strip())
                    if codigo == 0 or not codigo:
                        os.system("clear")
                        return main()
                except ValueError:
                    print("Por favor, insira um código válido.")
                    continue

                produtos = db_pro.carregar_produtos()
                cod_exist = False

                for prod in produtos:
                    if prod['codigo'] == codigo and prod['marca'] != "deleted":
                        cod_exist = True
                        nome = prod['nome']
                        preco = float(prod['preco'])
                        marca = prod['marca']
                        local = prod['local']
                        condicao = "exist"
                        break

                if not cod_exist:
                    while True:
                        nome = input("Nome do produto: ").strip()
                        if nome == "0" or nome == "":
                            os.system("clear")
                            return main()
                        break

                    while True:
                        try:
                            preco = float(input("Preço do produto: "))
                            if preco == 0:
                                os.system("clear")
                                return main()
                            break
                        except ValueError:
                            print("Por favor, insira um valor numérico para o preço.")

                    while True:
                        marca = input("Marca do produto: ").strip()
                        if marca == "0" or marca == "":
                            os.system("clear")
                            return main()
                        break

                    while True:
                        local = input("Local onde está estocado: ").strip()
                        if local == "0" or local == "":
                            os.system("clear")
                            return main()
                        break
                        
                while True:
                    try:
                        tamanho = int(input("Tamanho do produto: "))
                        if tamanho == 0:
                            os.system("clear")
                            return main()
                        break
                    except ValueError:
                        print("Por favor, insira um valor numérico para o tamanho.")

                while True:
                    cor = input("Cor do produto: ").strip()
                    if cor == "0" or cor == "":
                        os.system("clear")
                        return main()
                    break

                while True:
                    try:
                        quantidade = int(input("Quantidade do produto: "))
                        if quantidade == 0:
                            os.system("clear")
                            return main()
                        break
                    except ValueError:
                        print("Por favor, insira um valor numérico para a quantidade.")

                funcoes_pro.adicionar_produto(codigo, nome, preco, tamanho, cor, local, marca, quantidade, condicao)


        elif menu == "2":
            codigo = input("Insira o código do produto: ")
            os.system("clear")
            funcoes_pro.buscar_produto(codigo)

        elif menu == "3":
            os.system("clear")
            funcoes_pro.relatorio_pro()

        elif menu == "0":
            os.system('clear')
            menu_principal.main()
        else:
            os.system('clear')
            print("\nX Opção inválida X\n")