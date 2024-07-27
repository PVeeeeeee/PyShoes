import os

from tabulate import tabulate

import modulos.produtos.db_pro as db_pro
import modulos.produtos.menu_pro as menu_pro


def veri_nomepro(nome):
    produtos = db_pro.carregar_produtos()
    for prod in produtos:
        if nome.strip().lower() == prod['nome'].strip().lower():
            return True, prod
    return False, None


def adicionar_produto(codigo, nome, preco, tamanho, cor, local, marca, quantidade, condicao=None):
    try:
        produtos = db_pro.carregar_produtos()

        prod_cd = [prod for prod in produtos if prod['codigo'] == codigo]
        number = max(prod['number'] for prod in prod_cd) + 1 if prod_cd else 1

        produto = {
            "codigo": codigo,
            "number": number,
            "nome": nome,
            "preco": preco,
            "tamanho": tamanho,
            "cor": cor,
            "local": local,
            "marca": marca,
            "quantidade": quantidade,
            "marcador": ""
        }

        os.system("clear")

        produto_existe = False
        n, prodt = None, None

        for prod in produtos:
            if (produto['codigo'] == prod['codigo'] and produto['tamanho'] == prod['tamanho'] and produto['cor'].lower().strip() == prod['cor'].lower().strip()):
                produto_existe = True
                n = prod['number']
                prodt = prod
                break

        if produto_existe:
            if prodt and prodt.get('marcador') == "deleted":
                prodt['marcador'] = ""
                prodt['quantidade'] = quantidade
                print(f"Produto específico já existente (codigo: {codigo} número: {n})")
                db_pro.salvar_produtos(produtos)
                return menu_pro.main()
            else:
                print(f"Produto específico já existente (codigo: {codigo} número: {n})")
                return menu_pro.main()
        else:
            if condicao == "exist":
                print(f"Produto adicionado como: {nome} (codigo: {codigo} número: {n})\n")
            else:
                print("Produto adicionado com sucesso!\n")

            produtos.append(produto)
            db_pro.salvar_produtos(produtos)
            return menu_pro.main()

    except Exception as e:
        os.system("clear")
        print(f"Erro ao adicionar produto: {e}")





def buscar_produto(codigo):
    #try:
        if codigo == "0" or codigo.strip() == "":
            os.system("clear")
            return
            
        produtos = db_pro.carregar_produtos()
        
        produtos_encontrados = [prod for prod in produtos if int(prod["codigo"]) == int(codigo) and prod['marcador'] != "deleted"]

        if not produtos_encontrados:
            print("Produto não encontrado.\n")
        else:
            print("Produtos encontrados:")

            #tabela formatada pelo chatgpt
            headers = ["Código", "Número", "Nome", "Preço", "Tamanho", "Cor", "Local", "Marca", "Quantidade"]
            table = [
                [
                    produto['codigo'],
                    produto['number'],
                    produto['nome'],
                    produto['preco'],
                    produto['tamanho'],
                    produto['cor'],
                    produto['local'],
                    produto['marca'],
                    produto['quantidade']
                ]
                for produto in produtos_encontrados
            ]
            print(tabulate(table, headers=headers, tablefmt="rounded_grid", floatfmt=".2f"))
    
            sub_menu = input("\nO que você quer fazer?\n1- Editar produto\n2- Deletar produto\n0- Voltar\n")
        
            if sub_menu == "1":
                if len(produtos_encontrados) > 1:
                    number = input("Insira o N° do produto: ")
                else:
                    number = int(produtos_encontrados[0]["number"])
                editar_produto(codigo, number)
            elif sub_menu == "2":
                if len(produtos_encontrados) > 1:
                    number = input("Insira o N° do produto: ")
                else:
                    number = int(produtos_encontrados[0]["number"])
                deletar_produto(codigo, number)
            elif sub_menu == "0":
                os.system("clear")
                return
            else:
                os.system("clear")
                print("Opção inválida.")

    #except Exception as e:
      #  print(f"Erro ao exibir produto: {e}")




def editar_produto(codigo, number):
    #try:
        produtos = db_pro.carregar_produtos()

        if str(number) == "0" or  str(number).strip() == "":
            os.system("clear")
            return
        
        produto_enviado = next((prod for prod in produtos if int(prod["codigo"]) == int(codigo) and int(prod["number"]) == int(number) and prod["marcador"] != "deleted"), None)
    
        if not produto_enviado:
            os.system("clear")
            print("Número de produto inválido.")
            return
        else:
            produto = produto_enviado
                
            while True:
                try:
                    quantidade = input("Nova quantidade: ") or int(produto["quantidade"])
                    if int(quantidade) < 0:
                        os.system("clear")
                        return
                    produto["quantidade"] = int(quantidade)
                except Exception:
                    os.system("clear")
                    print("Use um valor numérico na quantidade\n")
                    return
                nome = input("Novo nome: ")
                if nome == "0":
                    os.system("clear")
                    return
                if nome:
                    for prod in produtos:
                        if int(prod['codigo']) == int(codigo):
                            prod['nome'] = nome
                try:
                    preco = (input("Novo preço: "))
                    if preco == "0":
                        os.system("clear")
                        return
                    if preco and preco.strip() != "":
                        for prod in produtos:
                            if int(prod['codigo']) == int(codigo):
                                prod['preco'] = float(preco)
                except Exception:
                    os.system("clear")
                    print("Use um valor numérico para o preço\n")
                    return
                try:
                    tamanho = input("Novo tamanho: ") or int(produto["tamanho"])
                    if int(tamanho) < 1:
                        os.system("clear")
                        return
                    produto["tamanho"] = int(tamanho)
                except Exception:
                    os.system("clear")
                    print("Use um valor numérico para tamanho\n")
                    return
                cor = input("Nova cor: ") or produto["cor"]
                if cor == "0":
                    os.system("clear")
                    return
                produto["cor"] = cor
                local = input("Novo local: ")
                if local == "0":
                    os.system("clear")
                    return
                if local:
                    for prod in produtos:
                        if int(prod['codigo']) == int(codigo):
                            prod['local'] = local
                marca = input("Nova marca: ")
                if marca == "0":
                    os.system("clear")
                    return
                if marca:
                    for prod in produtos:
                        if int(prod['codigo']) == int(codigo):
                            prod["marca"] = marca
                break

            db_pro.salvar_produtos(produtos)
            os.system("clear")
            print("Produto editado com sucesso!\n")
            return buscar_produto(codigo)
            
    #except Exception as e:
       # print(f"Erro ao editar produto: {e}")




def deletar_produto(codigo, number):
    try:
        produtos = db_pro.carregar_produtos()
        
        if str(number) == "0" or  str(number).strip() == "":
            os.system("clear")
            return

        produto_enviado = next((prod for prod in produtos if int(prod["codigo"]) == int(codigo) and int(prod["number"]) == int(number) and prod["marcador"] != "deleted"), None)

        if not produto_enviado:
            os.system("clear")
            print("Número de produto inválido.")
            return
        else:
            produto_enviado.update({
                'marcador': "deleted"
            })

            db_pro.salvar_produtos(produtos)
            os.system("clear")
            print("Produto deletado com sucesso!\n")
            
    except Exception as e:
        print(f"Erro ao deletar produto: {e}")



#ordenação feito pelo chatgpt

def relatorio_pro():
    try:
        produtos = db_pro.carregar_produtos()

        produto = [prod for prod in produtos if prod['marcador'] != "deleted"]

        produtos_ordenados = sorted(produto, key=lambda p: p['nome'])
        headers = ["Código", "Número", "Nome", "Preço", "Tamanho", "Cor", "Local", "Marca", "Quantidade"]
        table = [
            [
                produto['codigo'],
                produto['number'],
                produto['nome'],
                produto['preco'],
                produto['tamanho'],
                produto['cor'],
                produto['local'],
                produto['marca'],
                produto['quantidade']
            ]
            for produto in produtos_ordenados
        ]

        print(tabulate(table, headers=headers, tablefmt="rounded_grid", floatfmt=".2f"))

        submenu = input("0- Voltar\n")
        if submenu == "0":
            os.system("clear")
            return
        else:
            os.system("clear")
            return

    except Exception as e:
        print(f"Erro ao exibir relatório: {e}")
