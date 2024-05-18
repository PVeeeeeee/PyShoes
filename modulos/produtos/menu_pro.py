import modulos.produtos.funcoes_pro as funcoes_pro


def main():
    while True:
        menu = input('''O que você quer fazer?
    1- Adicionar novo produto
    2- Checar Produto
    0- Menu Principal
    ''')

        if menu == "1":
            nome = input("Nome do produto: ")
            while True:
                try:
                    preco = float(input("Preço do produto: "))
                    break
                except ValueError:
                    print("Por favor, insira um valor numérico para o preço.")
            codigo = input("Código do produto: ")
            while True:
                try:
                    tamanho = int(input("Tamanho do produto: "))
                    break
                except ValueError:
                    print("Por favor, insira um valor numérico para o tamanho.")
            cor = input("Cor do produto: ")
            modelo = input("Modelo do produto: ")
            marca = input("Marca do produto: ")
            while True:
                try:
                    quantidade = int(input("Quantidade do produto: "))
                    break
                except ValueError:
                    print("Por favor, insira um valor numérico para a quantidade.")

            funcoes_pro.adicionar_produto(nome, preco, codigo, tamanho, cor, modelo, marca, quantidade)

        elif menu == "2":
            codigo = input("Insira o código do produto: ")
            funcoes_pro.buscar_produto(codigo)

        elif menu == "0":
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()