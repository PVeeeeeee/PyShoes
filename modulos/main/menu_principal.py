import os
import sys

import modulos.pessoas.menu_pes as menu_pes
import modulos.produtos.menu_pro as menu_pro
import modulos.vendas.menu_ven as menu_ven


def main():
    while True:
        menu = input('''::::MENU PRINCIPAL::::
        
1- Menu de Vendas
2- Menu de Produtos
3- Menu de Pessoas
0- Sair

''').strip()
        if menu == "1":
            os.system('clear')
            menu_ven.main()
        elif menu == "2":
            os.system('clear')
            menu_pro.main()
        elif menu == "3":
            os.system('clear')
            menu_pes.main()
        elif menu == "0":
            os.system('clear')
            print(":::::::FIM DO PROGRAMA:::::::")
            sys.exit()
        else:
            os.system('clear')
            print("\nX Opção inválida X\n")
            