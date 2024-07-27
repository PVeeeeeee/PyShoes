import os
from datetime import datetime

from pytz import timezone
from tabulate import tabulate

import modulos.pessoas.db_pes as db_pes
import modulos.pessoas.funcoes_cli as funcoes_cli
import modulos.pessoas.funcoes_fun as funcoes_fun
import modulos.pessoas.funcoes_pes as funcoes_pes
import modulos.produtos.db_pro as db_pro
import modulos.vendas.db_ven as db_ven
import modulos.vendas.menu_ven as menu_ven


def vender_produto(codigo, cpf_cliente, cpf_vendedor):
    try:

        pessoas = db_pes.carregar_pessoas()
        produtos = db_pro.carregar_produtos()
        vendas = db_ven.carregar_vendas()

        id = max(venda['id'] for venda in vendas) + 1 if vendas else 1

        produtos_encontrados = [prod for prod in produtos if int(prod["codigo"]) == int(codigo) and prod['marcador'] != "deleted"]


        if len(produtos_encontrados) > 1:
            print("Produtos encontrados:")
            #produtos_reduzidos feito pelo chatgpt
            produtos_reduzidos = [dict(list(produto.items())[1:9]) for produto in produtos_encontrados]
            print(tabulate(produtos_reduzidos, headers="keys", tablefmt="pretty", floatfmt=".2f"))
            
            while True:
                produto_number = int(input("\nDigite o N° do produto que deseja vender: "))
                
                produto_valido = any(prod['number'] == (produto_number) for prod in produtos_encontrados)

                if produto_number == 0:
                    os.system("clear")
                    return

                if not produto_valido:
                    print("Esse número não pertence a um produto existente")
                else:
                    produto_para_venda = next((pro for pro in produtos_encontrados if pro['number'] == produto_number), None)
                    if produto_para_venda:
                        if produto_para_venda['quantidade'] == 0:
                            print("Produto sem estoque")
                        else:
                            break
                    else:
                        print('Produto Inválido')
        else:
            produto_para_venda = produtos_encontrados[0]
            if produto_para_venda['quantidade'] == 0:
                os.system("clear")
                print("Produto não pode ser vendido. Sem estoque.")
                return menu_ven.main()

        cliente = pessoas['clientes'][cpf_cliente]
        vendedor = pessoas['vendedores'][cpf_vendedor]

        venda = {
            "id": id,
            "codigo_produto": codigo,
            "produto_number": produto_para_venda["number"],
            "valor": produto_para_venda["preco"],
            "produto_nome": produto_para_venda['nome'],
            "cpf_cliente": cpf_cliente,
            "cliente_nome": cliente["nome"],
            "cliente_telefone": cliente["telefone"],
            "cpf_vendedor": cpf_vendedor,
            "vendedor_nome": vendedor["nome"],
            "vendedor_telefone": vendedor["telefone"],
            "data_venda": datetime.now(timezone('America/Sao_Paulo')).strftime("%d/%m/%y %H:%M"),
            "data_edit": "Nunca editado"
        }

        vendas.append(venda)
        db_ven.salvar_vendas(vendas)


        produto_para_venda['quantidade'] -= 1
        db_pro.salvar_produtos(produtos)


        if produto_para_venda["quantidade"] == 0:
            os.system("clear")
            print("Produto vendido e sem estoque!")
        else:
            os.system("clear")
            print("Produto vendido com sucesso!")

        funcoes_cli.calcular_prodcom()
        funcoes_fun.calcular_prodven()
        funcoes_fun.calcular_comissao()

    except Exception as e:
        print(f"Erro ao vender produto: {e}")




def buscar_venda(codigo=None, cpf=None, venda_edit=None):
    try:

        pessoas = db_pes.carregar_pessoas()
        produtos = db_pro.carregar_produtos()
        vendas = db_ven.carregar_vendas()
        vendas_encontradas = []
        
        for venda in vendas:

            # lõgica de filtragem feita pelo chatGPT
            
            if codigo and int(venda["codigo_produto"]) != int(codigo):
                continue
            if cpf and venda["cpf_cliente"] != cpf and venda["cpf_vendedor"] != cpf:
                continue
            if venda_edit and venda["cpf_cliente"] != venda_edit['cpf_cliente'] and venda["cpf_vendedor"] != venda_edit['cpf_vendedor'] and int(venda_edit['codigo_produto']) != int(venda['codigo_produto']):
                continue

            produto_nome = venda["produto_nome"]
            prod_ven =[prod for prod in produtos if int(venda['codigo_produto']) == int(prod['codigo']) and int(venda['produto_number']) == int(prod['number'])]
            
            if not prod_ven:
                produto_nome = venda["produto_nome"] + " (D)"
            else:
                for prod in prod_ven:
                    if prod["marcador"] == "deleted":
                         produto_nome = venda["produto_nome"] + " (D)"
                    elif prod['quantidade'] == 0:
                        produto_nome = venda["produto_nome"] + " (S)"
                        
            
            cliente = pessoas['clientes'].get(venda["cpf_cliente"])
            vendedor = pessoas['vendedores'].get(venda["cpf_vendedor"])
            if not cliente:
                cliente_nome = venda["cliente_nome"] + " (D)"
            elif cliente['nome'].lower().strip() != venda['cliente_nome'].lower().strip():
                cliente_nome = cliente['nome'] + " (E)"
            else:
                cliente_nome = cliente['nome']
            if not vendedor:
                vendedor_nome = venda["vendedor_nome"] + " (D)"
            elif vendedor['nome'].lower().strip() != venda['vendedor_nome'].lower().strip():
                vendedor_nome = vendedor['nome'] + " (E)"
            else:
                vendedor_nome = vendedor['nome']
                
            if not cliente:
                cliente_telefone = venda['cliente_telefone']
            elif cliente['telefone'].strip() != venda['cliente_telefone'].strip():
                cliente_telefone = cliente['telefone'] + " (E)"
            else:
                cliente_telefone = cliente['telefone']
            if not vendedor:
                vendedor_telefone = venda['vendedor_telefone']
            elif vendedor['telefone'].strip() != venda['vendedor_telefone'].strip():
                vendedor_telefone = vendedor['telefone'] + " (E)"
            else:
                vendedor_telefone = vendedor['telefone']
  
            


            venda_formatada = {
                "id": venda["id"],
                "Produto": produto_nome,
                "Código": f"{venda['codigo_produto']} ({venda['produto_number']})",
                "Valor": venda["valor"],
                "Cliente": cliente_nome + "\n" + venda["cpf_cliente"] + "\n" + cliente_telefone,
                "Vendedor": vendedor_nome + "\n" + venda["cpf_vendedor"]+ "\n" + vendedor_telefone,
                "Data": venda["data_venda"] + "\n" + venda["data_edit"]
            }
            vendas_encontradas.append(venda_formatada)

        if not vendas_encontradas:
            if codigo:
                os.system("clear")
                print(f"Nenhuma venda encontrada com o código de produto '{codigo}'.")
            elif cpf:
                os.system("clear")
                print(f"Nenhuma venda encontrada com o CPF '{cpf}'.")
        else:
            print("\nVendas encontradas:")
            print(tabulate(vendas_encontradas, headers="keys", tablefmt="pretty"))

            while True:
                sub_menu = input("\nO que você quer fazer?\n1- Editar venda\n2- Deletar venda\n0- Voltar\n")
                if sub_menu == "1":
                    if len(vendas_encontradas) > 1:
                        id_venda = (input("Insira o ID da venda: "))
                    else:
                        id_venda = vendas_encontradas[0]["id"]
                    editar_venda(id_venda)
                    break
                elif sub_menu == "2":
                    if len(vendas_encontradas) > 1:
                        id_venda = (input("Insira o ID da venda: "))
                    else:
                        id_venda = vendas_encontradas[0]["id"]
                    deletar_venda(id_venda)
                    break
                elif sub_menu == "0":
                    os.system("clear")
                    return
                else:
                    print("Opção inválida.")

        return vendas_encontradas
    except Exception as e:
        print(f"Erro ao buscar vendas: {e}")

#funçao ajustada e particionada pelo chatGPT

def editar_venda(id_venda):
    try:
        vendas = db_ven.carregar_vendas()
        produtos = db_pro.carregar_produtos()
        pessoas = db_pes.carregar_pessoas()

        if not id_venda or id_venda == "0":
            os.system("clear")
            return

        venda_para_editar = [venda for venda in vendas if int(venda["id"]) == int(id_venda)][0]
        if not venda_para_editar:
            os.system("clear")
            print(f"Venda com ID {id_venda} não encontrada.")
            return

        while True:
            novo_codigo = input("Insira o novo código do produto (deixe em branco para manter): ").strip()
    
            if novo_codigo == "0":
                os.system("clear")
                return
    
            if novo_codigo:
                produtos_encontrados = [prod for prod in produtos if int(prod["codigo"]) == int(novo_codigo) and prod['marcador'] != "deleted"]
                if produtos_encontrados:
                    produto_novo = selecionar_produto(produtos_encontrados)
                    if not produto_novo:
                        print("Produto não pode ser selecionado")
                    else:
                        break
                else:
                    print(f"Não existem produtos com o código: {novo_codigo}.")
            else:
                produto_novo = obter_produto_atual(produtos, venda_para_editar)
                if not produto_novo:
                    print("Produto escolhido não existe ou foi deletado.")
                else:
                    break

        while True:
            novo_cliente = input("Insira CPF do novo cliente (deixe em branco para manter): ").strip()
            if novo_cliente == "0":
                os.system("clear")
                return
    
            if novo_cliente:
                if not funcoes_pes.validar_cpf(novo_cliente):
                    print("CPF Inválido")
                if novo_cliente not in pessoas['clientes']:
                    cria_cliente(novo_cliente)
                    pessoas = db_pes.carregar_pessoas()
            break
        while True:
            novo_vendedor = input("Insira CPF do novo vendedor (deixe em branco para manter): ").strip()
            if novo_vendedor == "0":
                os.system("clear")
                return
    
            if novo_vendedor:
                if not funcoes_pes.validar_cpf(novo_vendedor):
                    print("CPF Inválido")
                    return
                if novo_vendedor not in pessoas['vendedores']:
                    print(f"Vendedor com CPF {novo_vendedor} não encontrado.")
                    return
            break

        atualizar_quantidades(produtos, venda_para_editar, produto_novo)

        venda_para_editar.update({
            "codigo_produto": produto_novo['codigo'],
            "valor": produto_novo['preco'],
            "produto_nome": produto_novo['nome'],
            "produto_number": produto_novo['number'],
            "cpf_cliente": novo_cliente or venda_para_editar["cpf_cliente"],
            "cliente_nome": pessoas['clientes'].get(novo_cliente, {}).get('nome', venda_para_editar["cliente_nome"]),
            "cliente_telefone": pessoas['clientes'].get(novo_cliente, {}).get('telefone', venda_para_editar["cliente_telefone"]),
            "cpf_vendedor": novo_vendedor or venda_para_editar["cpf_vendedor"],
            "vendedor_nome": pessoas['vendedores'].get(novo_vendedor, {}).get('nome', venda_para_editar["vendedor_nome"]),
            "vendedor_telefone": pessoas['vendedores'].get(novo_vendedor, {}).get('telefone', venda_para_editar["vendedor_telefone"]),
            "data_edit": datetime.now(timezone('America/Sao_Paulo')).strftime("%d/%m/%y %H:%M")
        })

        db_ven.salvar_vendas(vendas)
        db_pro.salvar_produtos(produtos)
        funcoes_cli.calcular_prodcom()
        funcoes_fun.calcular_prodven()
        funcoes_fun.calcular_comissao()

        os.system("clear")
        print("Venda editada com sucesso.")
        buscar_venda(venda_edit=venda_para_editar)

    except Exception as e:
        print(f"Erro ao editar venda: {e}")

def selecionar_produto(produtos_encontrados):
    if len(produtos_encontrados) > 1:
        print("Produtos encontrados:")
        print(tabulate(produtos_encontrados, headers="keys", tablefmt="pretty"))
        while True:
            try:
                produto_number = int(input("Insira o N° do produto: ")) - 1
                if produto_number == -1:
                    os.system("clear")
                    return None
                if 0 <= produto_number < len(produtos_encontrados):
                    produto_novo = produtos_encontrados[produto_number]
                    if produto_novo['quantidade'] > 0:
                        return produto_novo
                    else:
                        print("Produto sem estoque")
            except ValueError:
                print("Número Inválido")
    else:
        produto_novo = produtos_encontrados[0]
        if produto_novo['quantidade'] > 0:
            return produto_novo
        else:
            print("Produto sem estoque")
            return None

def obter_produto_atual(produtos, venda_para_editar):
    return next((prod for prod in produtos if int(prod["codigo"]) == int(venda_para_editar['codigo_produto']) and int(prod['number']) == int(venda_para_editar['produto_number']) and prod['marcador'] != "deleted"), None)

def atualizar_quantidades(produtos, venda_para_editar, produto_novo):
    produto_antigo = obter_produto_atual(produtos, venda_para_editar)
    if produto_antigo:
        produto_antigo['quantidade'] += 1
    produto_novo['quantidade'] -= 1



def cria_cliente(novo_cliente):
    print(f"Cliente com CPF {novo_cliente} não encontrado. Criando novo cliente...")
    while True:
        nome_novo_cli = input("Nome do Cliente: ")
        if nome_novo_cli.strip() == "0":
            os.system("clear")
            return menu_ven.main()
        if not funcoes_pes.verificar_nome(nome_novo_cli):
            print("Nome Inválido")
        else:
            break
    while True:
        telefone_novo_cli = input("Telefone do Cliente: ")
        if telefone_novo_cli.strip() == "0":
            os.system("clear")
            return menu_ven.main()
        if not funcoes_pes.verificar_telefone(telefone_novo_cli):
            print("Telefone Inválido")
        else:
            break

    funcoes_cli.adicionar_cli(nome_novo_cli, novo_cliente, telefone_novo_cli, "pass")
    return


def deletar_venda(id_venda):
    try:
        vendas = db_ven.carregar_vendas()
        produtos = db_pro.carregar_produtos()

        venda_para_deletar = [venda for venda in vendas if int(venda["id"]) == int(id_venda)][0]
        if not venda_para_deletar:
            print(f"Venda com ID {id_venda} não encontrada.")
            return

        codigo_produto = int(venda_para_deletar['codigo_produto'])
        produto_number = int(venda_para_deletar['produto_number'])

        produto = next((prod for prod in produtos if int(prod["codigo"]) == codigo_produto and int(prod["number"]) == produto_number), None)


        if produto:
            produto['quantidade'] += 1


        vendas.remove(venda_para_deletar)
        db_ven.salvar_vendas(vendas)
        db_pro.salvar_produtos(produtos)
        funcoes_cli.calcular_prodcom()
        funcoes_fun.calcular_prodven()
        funcoes_fun.calcular_comissao()
        os.system("clear")
        print("Venda deletada com sucesso.")
        
    except Exception as e:
        print(f"Erro ao deletar venda: {e}")



def relatorio_ven():
    try:
        vendas = db_ven.carregar_vendas()

        for venda in vendas:
            print(tabulate(venda.items(), headers="firstrow", tablefmt="grid")+"\n")
        submenu = input("0- Voltar\n")
        if submenu == "0":
            os.system("clear")
            return
        else:
            os.system("clear")
            return

    except Exception as e:
        print(f"Erro ao exibir relatório: {e}")