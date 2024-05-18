import modulos.pessoas.db_pes as db_pes
import modulos.pessoas.funcoes_cli as funcoes_cli
import modulos.pessoas.funcoes_pes as funcoes_pes
import modulos.produtos.db_pro as db_pro
import modulos.vendas.funcoes_ven as funcoes_ven


def main():
    while True:
        menu = input('''O que você quer fazer?
    1- Vender Produto
    2- Checar Vendas
    0- Menu Principal
    ''')

        if menu == "1":
            try:
                produtos = db_pro.carregar_produtos()
                pessoas = db_pes.carregar_pessoas()
                

                while True:
                    codigo = input("Insira o código do produto: ")
                    produtos_encontrados = [
                        prod for prod in produtos if prod["codigo"] == codigo
                    ]

                    # Verifica se o código existe no banco de dados de produtos (simulado)
                    if produtos_encontrados:
                        break
                    else:
                        print("Código de produto não encontrado. Tente novamente.")

                while True:
                    cpf_cliente = input("Insira o CPF do cliente: ")

                    # Verifica se o CPF é válido
                    if not funcoes_pes.validar_cpf(cpf_cliente):
                        print("Por favor, insira um CPF válido.")
             

                    else:
                        if cpf_cliente in pessoas['vendedores']:
                            print(f"CPF {cpf_cliente} pertence a um vendedor.")
                            
                        elif cpf_cliente not in pessoas['clientes']:
                            print(f"Cliente com CPF {cpf_cliente} não encontrado. Criando novo cliente...")
                            nome_cliente = input("Nome do Cliente: ")
                            funcoes_cli.adicionar_cli(nome_cliente, cpf_cliente)
                            break
                        else:
                            break

                while True:
                    cpf_vendedor = input("Insira o CPF do vendedor: ")

                    # Verifica se o vendedor existe no banco de dados (simulado)
                    if cpf_vendedor not in pessoas['vendedores']:
                        print(f"Vendedor com CPF {cpf_vendedor} não encontrado.")
                    else:
                        break

                funcoes_ven.vender_produto(codigo, cpf_cliente, cpf_vendedor)

            except Exception as e:
                print(f"Ocorreu um erro inesperado: {e}")

        elif menu == "2":
            try:
                dado_de_busca = input("Insira o código do produto ou CPF do cliente/vendedor: ")
                if funcoes_pes.validar_cpf(dado_de_busca):
                    funcoes_ven.buscar_venda(cpf=dado_de_busca)
                else:
                    funcoes_ven.buscar_venda(codigo=dado_de_busca)

            except Exception as e:
                print(f"Ocorreu um erro inesperado: {e}")

        elif menu == "0":
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
