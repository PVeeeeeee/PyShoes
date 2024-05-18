from datetime import datetime

from pytz import timezone

import modulos.pessoas.db_pes as db_pes
import modulos.pessoas.funcoes_pes as funcoes_pes

data_now = datetime.now(timezone('America/Sao_Paulo')).strftime("%d/%m/%Y %H:%M")


def adicionar_cli(nome, cpf):
    try:
        pessoas = db_pes.carregar_pessoas()
        cliente = {
            'nome': nome,
            'cpf': cpf,
            'funcao': "Cliente",
            'data_de_cadastro': data_now,
            'situacao': "EM DIA",
            'produtos_comprados': 0,
            'nivel_cliente': "Bronze"
        }

        pessoas['clientes'][cpf] = cliente
        db_pes.salvar_pessoas(pessoas)
        print("Cliente adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar cliente: {e}")

def editar_cli(cpf):
    try:
        pessoas = db_pes.carregar_pessoas()
        cliente = pessoas['clientes'][cpf] 
        print("Editar cliente:")
        
        cliente["nome"] = input("Novo nome: ") or cliente["nome"]
        
        while True:
            novo_cpf = input("Novo CPF: ")
            if novo_cpf:
                if funcoes_pes.validar_cpf(novo_cpf):
                    if not funcoes_pes.verificar_existencia(novo_cpf):
                        cliente['cpf'] = novo_cpf
                        break
                    else:
                        print("CPF já cadastrado.")
                else:
                    print("CPF inválido.")
            else:
                break
        
        while True:
            situacao = input(
                "Nova situação (Pendente/Em dia): "
            ).upper()
            if situacao:
                if situacao in ["PENDENTE", "EM DIA"]:
                    cliente['situacao'] = situacao
                    break
                else:
                    print("Situação inválida.")
            else:
                break
                
        db_pes.salvar_pessoas(pessoas)
        print("Cliente editado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao editar cliente: {e}")
