from datetime import datetime

from pytz import timezone
from tabulate import tabulate

import modulos.pessoas.db_pes as db_pes
import modulos.pessoas.funcoes_cli as funcoes_cli
import modulos.pessoas.funcoes_fun as funcoes_fun
import modulos.pessoas.funcoes_pes as funcoes_pes
import modulos.produtos.db_pro as db_pro
import modulos.vendas.db_ven as db_ven

data_now = datetime.now(timezone('America/Sao_Paulo')).strftime("%d/%m/%y %H:%M")

def vender_produto(codigo, cpf_cliente, cpf_vendedor):
    try:
        pessoas = db_pes.carregar_pessoas()
        produtos = db_pro.carregar_produtos()
        vendas = db_ven.carregar_vendas()

        id = max(venda['id'] for venda in vendas) + 1 if vendas else 1

        produtos_encontrados = [prod for prod in produtos if prod["codigo"] == codigo]

        if not produtos_encontrados:
            print("Produto não encontrado.")
            return

        if len(produtos_encontrados) > 1:
            print("Produtos encontrados:")
            print(tabulate(produtos_encontrados, headers="keys", tablefmt="pretty"))
            numero_produto = int(input("\nDigite o N° do produto que deseja vender: "))
            produto_para_venda = next((prod for prod in produtos_encontrados if prod["number"] == numero_produto), None)
            if not produto_para_venda:
                print("Número de produto inválido.")
                return
            elif produto_para_venda['quantidade'] == 0:
                print('Produto sem estoque')
                return
        else:
            produto_para_venda = produtos_encontrados[0]

        venda = {
            "id": id,
            "valor": produto_para_venda["preco"],
            "codigo_produto": codigo,
            "produto_nome": produto_para_venda['nome'],
            "produto_number": produto_para_venda["number"],
            "cpf_cliente": cpf_cliente,
            "cpf_vendedor": cpf_vendedor,
            "data_venda": data_now
        }

        cliente = pessoas['clientes'][cpf_cliente]
        vendedor = pessoas['vendedores'][cpf_vendedor]

        vendedor["produtos_vendidos"] += produto_para_venda["preco"]
        cliente["produtos_comprados"] += produto_para_venda["preco"]
        db_pes.salvar_pessoas(pessoas)

        if produto_para_venda["quantidade"] == 1:
            print("Produto vendido e sem estoque!")
        else:
            produto_para_venda["quantidade"] -= 1
            print("Produto vendido com sucesso!")

        db_ven.registrar_venda(venda)
        db_pro.salvar_produtos(produtos)

        funcoes_fun.calcular_comissao()

    except Exception as e:
        print(f"Erro ao vender produto: {e}")




def buscar_venda(codigo=None, cpf=None):
    try:
        vendas = db_ven.carregar_vendas()
        pessoas = db_pes.carregar_pessoas()
        produtos = db_pro.carregar_produtos()

        vendas_encontradas = []
        for venda in vendas:
            if codigo and venda["codigo_produto"] != codigo:
                continue
            if cpf and venda["cpf_cliente"] != cpf and venda["cpf_vendedor"] != cpf:
                continue

            produto = next((prod for prod in produtos if prod["codigo"] == venda["codigo_produto"]), None)
            cliente = pessoas['clientes'].get(venda["cpf_cliente"])
            vendedor = pessoas['vendedores'].get(venda["cpf_vendedor"])

            if produto and cliente and vendedor:
                venda_formatada = {
                    "id": venda["id"],
                    "Produto_nome": venda["produto_nome"],
                    "Código": f"{venda['codigo_produto']} ({venda['produto_number']})",
                    "Valor": venda["valor"],
                    "Cliente": cliente["nome"],
                    "Vendedor": vendedor["nome"],
                    "Data": venda["data_venda"]
                }
                vendas_encontradas.append(venda_formatada)

        if not vendas_encontradas:
            if codigo:
                print(f"Nenhuma venda encontrada com o código de produto '{codigo}'.")
            elif cpf:
                print(f"Nenhuma venda encontrada com o CPF '{cpf}'.")
        else:
            print("\nVendas encontradas:")
            print(tabulate(vendas_encontradas, headers="keys", tablefmt="pretty"))

            while True:
                sub_menu = input("\nO que você quer fazer?\n1- Editar venda\n2- Deletar venda\n0- Voltar\n")
                if sub_menu == "1":
                    if len(vendas_encontradas) > 1:
                        id_venda = int(input("Insira o ID da venda: "))
                    else:
                        id_venda = vendas_encontradas[0]["id"]
                    editar_venda(id_venda)
                    break
                elif sub_menu == "2":
                    if len(vendas_encontradas) > 1:
                        id_venda = int(input("Insira o ID da venda: "))
                    else:
                        id_venda = vendas_encontradas[0]["id"]
                    deletar_venda(id_venda)
                    break
                elif sub_menu == "0":
                    return
                else:
                    print("Opção inválida.")

        return vendas_encontradas
    except Exception as e:
        print(f"Erro ao buscar vendas: {e}")


def editar_venda(id_venda):
    try:
        vendas = db_ven.carregar_vendas()
        produtos = db_pro.carregar_produtos()
        pessoas = db_pes.carregar_pessoas()

        venda_para_editar = next((venda for venda in vendas if venda["id"] == id_venda), None)
        if not venda_para_editar:
            print(f"Venda com ID {id_venda} não encontrada.")
            return

        while True:
            novo_codigo = input("Insira o novo código do produto (deixe em branco para manter): ").strip() or venda_para_editar["codigo_produto"]
            produtos_encontrados = [prod for prod in produtos if prod["codigo"] == novo_codigo]

            if not produtos_encontrados:
                print("Produto não encontrado.\n")
            else:
                print("\nProdutos encontrados:")
                for produto in produtos_encontrados:
                    print(tabulate([produto], headers="keys", tablefmt="pretty"))
                if len(produtos_encontrados) > 1:
                    number = int(input("Insira o N° do produto: ")) - 1
                else:
                    number = 0
                produto_novo = produtos_encontrados[number]
                break

        while True:
            novo_cliente = input("Insira CPF do novo cliente (deixe em branco para manter): ").strip() or venda_para_editar["cpf_cliente"]

            if not funcoes_pes.validar_cpf(novo_cliente):
                print("Por favor, insira um CPF válido.")
            else:
                if novo_cliente in pessoas['vendedores']:
                    print(f"CPF {novo_cliente} pertence a um vendedor.")
                elif novo_cliente not in pessoas['clientes']:
                    print(f"Cliente com CPF {novo_cliente} não encontrado. Criando novo cliente...")
                    nome_cliente = input("Nome do Cliente: ")
                    cpf_cliente = novo_cliente
                    funcoes_cli.adicionar_cli(nome_cliente, cpf_cliente)
                    pessoas = db_pes.carregar_pessoas() 
                    cliente_novo = pessoas['clientes'][novo_cliente]
                    break
                else:
                    cliente_novo = pessoas['clientes'][novo_cliente]
                    break

        while True:
            novo_vendedor = input("Insira CPF do novo vendedor (deixe em branco para manter): ").strip() or venda_para_editar["cpf_vendedor"]

            if novo_vendedor not in pessoas['vendedores']:
                print(f"Vendedor com CPF {novo_vendedor} não encontrado.")
            else:
                vendedor_novo = pessoas['vendedores'][novo_vendedor]
                break

        cliente_antigo = pessoas['clientes'].get(venda_para_editar["cpf_cliente"])
        vendedor_antigo = pessoas['vendedores'].get(venda_para_editar["cpf_vendedor"])
        valor_antigo = venda_para_editar['valor']
        valor_novo = produto_novo['preco']
        produto_antigo = next((prod for prod in produtos if prod["codigo"] == venda_para_editar['codigo_produto'] and prod["number"] == venda_para_editar['produto_number']), None)

        if cliente_antigo and novo_cliente != venda_para_editar['cpf_cliente']:
            cliente_antigo['produtos_comprados'] -= valor_antigo
        if cliente_novo:
            if novo_cliente != venda_para_editar['cpf_cliente']:
                cliente_novo['produtos_comprados'] += valor_novo
            elif novo_codigo != venda_para_editar['codigo_produto']:
                cliente_novo['produtos_comprados'] -= valor_antigo
                cliente_novo['produtos_comprados'] += valor_novo

        if vendedor_antigo and novo_vendedor != venda_para_editar['cpf_vendedor']:
            vendedor_antigo['produtos_vendidos'] -= valor_antigo
        if vendedor_novo:
            if novo_vendedor != venda_para_editar['cpf_vendedor']:
                vendedor_novo['produtos_vendidos'] += valor_novo
            elif novo_codigo != venda_para_editar['codigo_produto']:
                vendedor_novo['produtos_vendidos'] -= valor_antigo
                vendedor_novo['produtos_vendidos'] += valor_novo

        if produto_antigo and (novo_codigo != venda_para_editar['codigo_produto'] or produto_novo['number'] != venda_para_editar['produto_number']):
            produto_antigo['quantidade'] += 1
            produto_novo['quantidade'] -= 1

        venda_editada = {
            "id": id_venda,
            "codigo_produto": produto_novo['codigo'],
            "produto_nome": produto_novo['produto_nome'],
            "produto_number": produto_novo['number'],
            "valor": produto_novo['preco'],
            "cpf_cliente": novo_cliente,
            "cpf_vendedor": novo_vendedor,
            "data_venda": data_now
        }

        vendas[vendas.index(venda_para_editar)] = venda_editada
        db_ven.salvar_vendas(vendas)
        db_pes.salvar_pessoas(pessoas)
        db_pro.salvar_produtos(produtos)
        funcoes_fun.calcular_comissao()
        print("Venda editada com sucesso!")

    except Exception as e:
        print(f"Erro ao editar venda: {e}")


def deletar_venda(id_venda):
    try:
        vendas = db_ven.carregar_vendas()
        pessoas = db_pes.carregar_pessoas()
        produtos = db_pro.carregar_produtos()

        venda_para_deletar = next((venda for venda in vendas if venda["id"] == id_venda), None)
        if not venda_para_deletar:
            print(f"Venda com ID {id_venda} não encontrada.")
            return

        confirmacao = input(f"Tem certeza que deseja deletar a venda com ID {id_venda}? (s/n): ")
        if confirmacao.lower() != 's':
            print("Operação cancelada.")
            return

        cliente = pessoas['clientes'].get(venda_para_deletar["cpf_cliente"])
        vendedor = pessoas['vendedores'].get(venda_para_deletar["cpf_vendedor"])
        produto = next((prod for prod in produtos if prod["codigo"] == venda_para_deletar["codigo_produto"]), None)

        if cliente:
            cliente["produtos_comprados"] -= venda_para_deletar["valor"]
        if vendedor:
            vendedor["produtos_vendidos"] -= venda_para_deletar["valor"]
        if produto:
            produto["quantidade"] += 1

        vendas.remove(venda_para_deletar)
        db_ven.salvar_vendas(vendas)
        db_pes.salvar_pessoas(pessoas)
        db_pro.salvar_produtos(produtos)
        funcoes_fun.calcular_comissao()
        print("Venda deletada com sucesso!")

    except Exception as e:
        print(f"Erro ao deletar venda: {e}")
