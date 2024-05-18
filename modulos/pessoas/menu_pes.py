import modulos.pessoas.funcoes_cli as funcoes_cli
import modulos.pessoas.funcoes_fun as funcoes_fun
import modulos.pessoas.funcoes_pes as funcoes_pes


def main():
    while True:
        menu = input('''O que você quer fazer?
    1- Adicionar Cliente
    2- Adicionar Vendedor 
    3- Checar pessoa
    0- Menu Principal
    ''')

        if menu == "1":
            nome = input("Nome do cliente: ")
            while True:
                cpf = input("CPF do cliente: ")
                if funcoes_pes.verificar_existencia(cpf):
                    print("CPF já está em uso. Por favor, insira um CPF válido.")
                elif not funcoes_pes.validar_cpf(cpf):
                    print("CPF inválido. Por favor, insira um CPF válido.")
                else:
                    break
            funcoes_cli.adicionar_cli(nome, cpf)

        elif menu == "2":
            nome = input("Nome do vendedor: ")
            while True:
                cpf = input("CPF do vendedor: ")
                if funcoes_pes.verificar_existencia(cpf):
                    print("CPF já está em uso. Por favor, insira um CPF válido.")
                elif not funcoes_pes.validar_cpf(cpf):
                    print("CPF inválido. Por favor, insira um CPF válido.")
                else:
                    break
            funcoes_fun.adicionar_ven(nome, cpf)

        elif menu == "3":
            cpf = input("Insira o CPF: ")
            funcoes_pes.buscar_pessoa(cpf)

        elif menu == "0":
            break

        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()