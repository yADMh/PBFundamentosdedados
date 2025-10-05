import psycopg2
from psycopg2 import Error

from config import DB_CONFIG

def criar_conexao():
    """
    Cria uma conexão com o banco de dados PostgreSQL.
    """
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabela(conn):
    """
    Cria a tabela de tarefas se ela não existir.
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id SERIAL PRIMARY KEY,
                descricao TEXT NOT NULL,
                tipo TEXT NOT NULL,
                data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Pendente',
                prazo DATE,
                urgencia TEXT DEFAULT 'Baixa'
            )
        """)
        conn.commit()
        print("Tabela 'tarefas' criada ou já existe.")
    except Error as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        cursor.close()
