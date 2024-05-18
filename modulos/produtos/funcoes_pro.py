from tabulate import tabulate

import modulos.produtos.db_pro as db_pro


def adicionar_produto(nome, preco, codigo, tamanho, cor, modelo, marca, quantidade):
    try:
        produtos = db_pro.carregar_produtos()
        max_number = max([prod["number"] for prod in produtos if prod["codigo"] == codigo], default=0)
        number = max_number + 1
        novo_produto = {
            "number": number,
            "nome": nome,
            "preco": preco,
            "codigo": codigo,
            "tamanho": tamanho,
            "cor": cor,
            "modelo": modelo,
            "marca": marca,
            "quantidade": quantidade
        }
        produtos.append(novo_produto)
        db_pro.salvar_produtos(produtos)
        print("\nProduto adicionado com sucesso!\n")
    except Exception as e:
        print(f"Erro ao adicionar produto: {e}")


def buscar_produto(codigo):
    produtos = db_pro.carregar_produtos()
    produtos_encontrados = [
        prod for prod in produtos if prod["codigo"] == codigo
    ]
    
    try:
        if not produtos_encontrados:
            print("Produto não encontrado.\n")
        else:
            print("\nProdutos encontrados:")
            for produto in produtos_encontrados:
                print(tabulate(produto.items(), tablefmt="pretty"))

            sub_menu = input("\nO que você quer fazer?\n1- Editar produto\n2- Deletar produto\n0- Voltar\n")
        
           
            if sub_menu == "1":
                if len(produtos_encontrados) > 1:
                    number = int(input("Insira o N° do produto: "))
                else:
                    number = produtos_encontrados[0]["number"]
                editar_produto(codigo, number)
            elif sub_menu == "2":
                if len(produtos_encontrados) > 1:
                    number = int(input("Insira o N° do produto: "))
                else:
                    number = produtos_encontrados[0]["number"]
                deletar_produto(codigo, number)
            elif sub_menu == "0":
                return
            else:
                print("Opção inválida.")

    except Exception as e:
        print(f"Erro: {e}")


def editar_produto(codigo, number):
    try:
        produtos = db_pro.carregar_produtos()
        produto = next(
            (prod for prod in produtos
             if prod["codigo"] == codigo and prod["number"] == number), None)
        if not produto:
            print("Produto não encontrado.")
        else:
            nome = input("Novo nome: ") or produto["nome"]
            preco = input("Novo preço: ") or produto["preco"]
            tamanho = input("Novo tamanho: ") or produto["tamanho"]
            cor = input("Nova cor: ") or produto["cor"]
            modelo = input("Novo modelo: ") or produto["modelo"]
            marca = input("Nova marca: ") or produto["marca"]
            quantidade = input("Nova quantidade: ") or produto["quantidade"]

            produto["nome"] = nome
            produto["preco"] = float(preco)
            produto["tamanho"] = int(tamanho)
            produto["cor"] = cor
            produto["modelo"] = modelo
            produto["marca"] = marca
            produto["quantidade"] = int(quantidade)

            db_pro.salvar_produtos(produtos)
            print("\nProduto editado com sucesso!\n")
    except Exception as e:
        print(f"Erro ao editar produto: {e}")


def deletar_produto(codigo, number):
    try:
        produtos = db_pro.carregar_produtos()
        produto = next(
            (prod for prod in produtos
             if prod["codigo"] == codigo and prod["number"] == number), None)
        if not produto:
            print("Produto não encontrado.")
        else:
            produtos.remove(produto)

            for prod in produtos:
                if prod["codigo"] == codigo and prod["number"] > number:
                    prod["number"] -= 1

            db_pro.salvar_produtos(produtos)
            print("\nProduto deletado com sucesso!\n")
    except Exception as e:
        print(f"Erro ao deletar produto: {e}")
