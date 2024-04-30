import sqlite3

conn = sqlite3.connect('produtos.db')
c = conn.cursor()

c.execute('''
      CREATE TABLE IF NOT EXISTS produtos (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          number INTEGER DEFAULT 1,
          nome TEXT,
          preco FLOAT,
          codigo INTEGER,
          tamanho INTEGER,
          cor TEXT,
          modelo TEXT,
          marca TEXT,
          quantidade INTEGER
      )
  ''')


def adicionar_produto(nome, preco, codigo, tamanho, cor, modelo, marca,
                      quantidade):
  try:

    c.execute('SELECT MAX(number) FROM produtos WHERE codigo = ?', (codigo, ))
    max_number = c.fetchone()[0]
    number = max_number + 1 if max_number else 1

    c.execute(
        '''
            INSERT INTO produtos (number, nome, preco, codigo, tamanho, cor, modelo, marca, quantidade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
        (number, nome, preco, codigo, tamanho, cor, modelo, marca, quantidade))

    print("Produto adicionado com sucesso!")
  except Exception as e:
    print(f"Erro ao adicionar produto: {e}")


def buscar_produto(codigo):
  try:

    c.execute(
        'SELECT number, nome, preco, codigo, tamanho, cor, modelo, marca, quantidade FROM produtos WHERE codigo = ?',
        (codigo, ))
    produtos = c.fetchall()

    if not produtos:
      print("Produto não encontrado.")
    else:
      print("\nProdutos encontrados:")
      for produto in produtos:
        print(produto)

      sub_menu = int(
          input(
              "\nO que você quer fazer?\n1- Editar produto\n2- Deletar produto\n"
          ))

      if len(produtos) > 1:
        number = int(input("Insira o N° do produto: "))
      else:
        number = produtos[0][0]

      if sub_menu == 1:
        nome = input("Novo nome do produto: ")
        while True:
          try:
            preco = float(input("Novo preço do produto: "))
            break
          except ValueError:
            print("Por favor, insira um valor numérico para o preço.")
        while True:
          try:
            tamanho = int(input("Novo tamanho do produto: "))
            break
          except ValueError:
            print("Por favor, insira um valor numérico para o tamanho.")
        cor = input("Nova cor do produto: ")
        modelo = input("Novo modelo do produto: ")
        marca = input("Nova marca do produto: ")
        while True:
          try:
            quantidade = int(input("Nova quantidade do produto: "))
            break
          except ValueError:
            print("Por favor, insira um valor numérico para a quantidade.")

        editar_produto(codigo, number, nome, preco, tamanho, cor, modelo,
                       marca, quantidade)
      elif sub_menu == 2:
        deletar_produto(codigo, number)
  except Exception as e:
    print(f"Erro ao buscar produto: {e}")


def editar_produto(codigo, number, nome, preco, tamanho, cor, modelo, marca,
                   quantidade):
  try:

    c.execute(
        'UPDATE produtos SET nome=?, preco=?, tamanho=?, cor=?, modelo=?, marca=?, quantidade=? WHERE codigo=? AND number=?',
        (nome, preco, tamanho, cor, modelo, marca, quantidade, codigo, number))

    print("Produto editado com sucesso!")
  except Exception as e:
    print(f"Erro ao editar produto: {e}")


def deletar_produto(codigo, number):
  try:

    c.execute('DELETE FROM produtos WHERE codigo=? AND number=?',
              (codigo, number))

    c.execute(
        'UPDATE produtos SET number=number-1 WHERE codigo=? AND number>?',
        (codigo, number))

    print("Produto deletado com sucesso!")
  except Exception as e:
    print(f"Erro ao deletar produto: {e}")


def vender_produto(codigo):
  try:

    c.execute(
        'SELECT number, nome, preco, codigo, tamanho, cor, modelo, marca, quantidade FROM produtos WHERE codigo = ?',
        (codigo, ))
    produtos = c.fetchall()

    if not produtos:
      print("Não há produtos com o código especificado.")
    else:
      print("\nProdutos encontrados:")
      for produto in produtos:
        print(produto)

      number = int(input("\nDigite o número do produto que deseja vender: "))

      c.execute('SELECT * FROM produtos WHERE codigo = ? and number = ?',
                (codigo, number))
      produto = c.fetchone()

      if produto:
        if produto[-1] > 0:
          nova_quantidade = produto[-1] - 1
          c.execute(
              'UPDATE produtos SET quantidade = ? WHERE codigo = ? and number = ?',
              (nova_quantidade, codigo, number))
          print("Produto vendido com sucesso!")
        else:
          print("Produto sem estoque")
      else:
        print("Produto não encontrado.")
  except Exception as e:
    print(f"Erro ao vender produto: {e}")


menu = int(
    input('''O que você quer fazer?
1- Vender produto
2- Checar produto
3- Adicionar novo produto
'''))

if menu == 1:
  codigo = input("Insira o código do produto: ")
  vender_produto(codigo)
elif menu == 2:
  codigo = input("Insira o código do produto: ")
  buscar_produto(codigo)
elif menu == 3:
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

  adicionar_produto(nome, preco, codigo, tamanho, cor, modelo, marca,
                    quantidade)
else:
  print("Opção inválida")

conn.commit()
conn.close()

#verificador de codigo de barras padrao EAN-13
'''
code = input("Insira o código do calçado: ")

if len(code) != 13 or not code.isdigit():
  print("Código inválido")
else:
  numbers = [int(code[i]) for i in range(12)]

  weights = [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3]

  total = sum(number * weight for number, weight in zip(numbers, weights))

  verification_digit = (((total//10)+1)*10)-total

  if verification_digit == int(code[12]):
      print("Válido")
  else:
      print("Inválido")
'''
