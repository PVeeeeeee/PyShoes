import modulos.pessoas.funcoes_fun as funcoes_fun
import modulos.pessoas.menu_pes as menu_pes
import modulos.produtos.menu_pro as menu_pro
import modulos.vendas.menu_ven as menu_ven


def main():
    while True:
        menu = input('''O que você quer fazer?
    1- Menu de Vendas
    2- Menu de Produtos
    3- Menu de Pessoas
    0- Sair
    ''')

        if menu == "1":
            menu_ven.main()
        elif menu == "2":
            menu_pro.main()
        elif menu == "3":
            menu_pes.main()
        elif menu == "0":
            break
        else:
            print("Opção inválida")


if __name__ == "__main__":
    main()
    funcoes_fun.calcular_comissao()
