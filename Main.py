import sqlite3


def criar_tabela_produtos():
  conn = sqlite3.connect('produtos.db')
  c = conn.cursor()

  c.execute('''
  CREATE TABLE IF NOT EXISTS produtos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      number INTEGER DEFAULT 1,
      nome TEXT,
      preco REAL,
      codigo INTEGER,
      tamanho INTEGER,
      cor TEXT,
      modelo TEXT,
      marca TEXT,
      quantidade INTEGER
  )
  ''')

  conn.commit()
  conn.close()

def adicionar_produto(nome, preco, codigo, tamanho, cor, modelo, marca, quantidade):
  conn = sqlite3.connect('produtos.db')
  c = conn.cursor()

  c.execute('SELECT COUNT(*) FROM produtos WHERE codigo = ?', (codigo,))
  count = c.fetchone()[0]

  if count > 0:
      c.execute('SELECT MAX(number) FROM produtos WHERE codigo = ?', (codigo,))
      max_number = c.fetchone()[0]
      number = max_number + 1
    
  else:
      pass

  c.execute('''
  INSERT INTO produtos (number, nome, preco, codigo, tamanho, cor, modelo, marca, quantidade)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
  ''', (number, nome, preco, codigo, tamanho, cor, modelo, marca, quantidade))

  conn.commit()
  conn.close()
  print("Produto adicionado com sucesso!")

def buscar_produto(codigo):
  conn = sqlite3.connect('produtos.db')
  c = conn.cursor()

  c.execute('SELECT number, nome, preco, codigo, tamanho, cor, modelo, marca, quantidade FROM produtos WHERE codigo = ?', (codigo,))
  produtos = c.fetchall()

  conn.close()

  if produtos:
    print("\nProdutos encontrados:")
    for produto in produtos:
      print(produto)
      
    editar_menu = int(input("\nO que você quer fazer?\n1- Editar produto\n2- Deletar produto\n"))

    if len(produtos) > 1:
      number = int(input("Insira o N° do produto: "))
    else:
      number = produtos[0][0]

    if editar_menu == 1:
      nome = input("Novo nome do produto: ")
      preco = float(input("Novo preço do produto: "))
      tamanho = input("Novo tamanho do produto: ")
      cor = input("Nova cor do produto: ")
      modelo = input("Novo modelo do produto: ")
      marca = input("Nova marca do produto: ")
      quantidade = int(input("Nova quantidade do produto: "))

      editar_produto(number, nome, preco, codigo, tamanho, cor, modelo, marca, quantidade)

    elif editar_menu == 2:
      deletar_produto(number, codigo)
      
  else:
    print("Produto não encontrado.")

def editar_produto(number, nome, preco, codigo, tamanho, cor, modelo, marca, quantidade):
  conn = sqlite3.connect('produtos.db')
  c = conn.cursor()
  c.execute('''
  UPDATE produtos
  SET nome = ?,
      preco = ?,
      tamanho = ?,
      cor = ?,
      modelo = ?,
      marca = ?,
      quantidade = ?
  WHERE codigo = ? and number = ?
  ''', (nome, preco, tamanho, cor, modelo, marca, quantidade, codigo, number))
  conn.commit()
  conn.close()

  print("Produto editado com sucesso!")
  
def deletar_produto(number, codigo):
  conn = sqlite3.connect('produtos.db')
  c = conn.cursor()

  c.execute('DELETE FROM produtos WHERE codigo = ? AND number = ?', (codigo, number))

  c.execute('SELECT number FROM produtos WHERE codigo = ? ORDER BY number', (codigo,))
  remaining_products = c.fetchall()

  for idx, row in enumerate(remaining_products, start=1):
      new_number = idx
      old_number = row[0]

      if new_number != old_number:
          c.execute('UPDATE produtos SET number = ? WHERE codigo = ? AND number = ?', (new_number, codigo, old_number))

  conn.commit()
  conn.close()
  print("Produto deletado com sucesso!")

def vender_produto(codigo):
  conn = sqlite3.connect('produtos.db')
  c = conn.cursor()

  c.execute('SELECT number, nome, preco, codigo, tamanho, cor, modelo, marca, quantidade FROM produtos WHERE codigo = ?', (codigo,))
  produtos = c.fetchall()

  if not produtos:
      print("Não há produtos com o código especificado.")
  else:
      print("\nProdutos encontrados:")
      for produto in produtos:
          print(produto)

      number = int(input("\nDigite o número do produto que deseja vender: "))

      c.execute('SELECT * FROM produtos WHERE codigo = ? and number = ?', (codigo, number))
      produto = c.fetchone()

      if produto:
          if produto[-1] > 0:
              nova_quantidade = produto[-1] - 1
              c.execute('UPDATE produtos SET quantidade = ? WHERE codigo = ? and number = ?', (nova_quantidade, codigo, number))
              conn.commit()
              print("Produto vendido com sucesso!")
          else:
              print("Produto sem estoque")
      else:
          print("Produto não encontrado.")

  conn.close()

criar_tabela_produtos()

menu = int(input('''O que você quer fazer?
1- Vender produto
2- Checar produto
3- Adicionar novo produto
'''))

if menu == 1:
  codigo = input("Insira o código do produto: ")
  vender_produto(codigo)
  
elif menu == 2:
  codigo = input("Insira o código do produto: ")
  produtos = buscar_produto(codigo)
  
elif menu == 3:
    nome = input("Nome do produto: ")
    preco = float(input("Preço do produto: "))
    codigo = input("Código do produto: ")
    tamanho = input("Tamanho do produto: ")
    cor = input("Cor do produto: ")
    modelo = input("Modelo do produto: ")
    marca = input("Marca do produto: ")
    quantidade = int(input("Quantidade do produto: "))
    
    adicionar_produto(nome, preco, codigo, tamanho, cor, modelo, marca, quantidade)
  
else:
    print("Opção inválida")



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
