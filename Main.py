import os

import modulos.main.menu_principal as menu_principal
import modulos.pessoas.funcoes_fun as funcoes_fun

if __name__ == "__main__":
  os.system("clear")
  print("Bem-vindo(a) ao PyShoes!!!\n")
  print("Comece criando pelo menos 1 cliente, funcionario e produto")
  print("Documento 'Sobre' o sistema disponível na pasta do projeto\n")

  funcoes_fun.calcular_comissao()
  menu_principal.main()