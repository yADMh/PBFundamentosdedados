import sys

from database import criar_conexao, criar_tabela
from ui import menu

# Iniciar o sistema
if __name__ == "__main__":
    conn = criar_conexao()
    if conn:
        criar_tabela(conn)
        conn.close()
    else:
        print("Falha na conexão com o banco de dados. Verifique as configurações em config.py.")
        sys.exit(1)
    print("Bem-vindo ao Sistema de Gestão de Montagem de Computador!")
    menu()
