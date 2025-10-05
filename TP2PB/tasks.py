import psycopg2
from psycopg2 import Error, sql

from database import criar_conexao

def adicionar_Tarefa(descricao, tipo="Nova", prazo=None, urgencia='Baixa'):
    """
    Adiciona uma nova Tarefa ao banco de dados PostgreSQL.

    :param descricao: Descrição da Tarefa.
    :param tipo: Tipo (Nova Peça ou Modificação).
    :param prazo: Data de prazo final (opcional, formato YYYY-MM-DD).
    :param urgencia: Nível de urgência (opcional, padrão é 'Baixa').
    """
    conn = criar_conexao()
    if conn is None:
        return
    
    cursor = None
    try:
        cursor = conn.cursor()
        # data_criacao é gerada automaticamente pela tabela (CURRENT_TIMESTAMP)
        # Mas para prazo, convertemos para DATE se fornecido
        cursor.execute("""
            INSERT INTO tarefas (descricao, tipo, prazo, urgencia)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (descricao, tipo, prazo, urgencia))
        
        new_id = cursor.fetchone()[0]
        conn.commit()
        print(f"{tipo} adicionada com ID {new_id}: {descricao}")
    except Error as e:
        print(f"Erro ao adicionar tarefa: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        conn.close()

def listar_Tarefas():
    """
    Lista todas as Tarefas do banco de dados PostgreSQL.
    """
    conn = criar_conexao()
    if conn is None:
        return
    
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tarefas ORDER BY id")
        tarefas = cursor.fetchall()
        
        if not tarefas:
            print("Nenhuma Tarefa registrada.")
            return
        
        print("\n=== LISTA DE TAREFAS ===")
        for tarefa in tarefas:
            id_tarefa, descricao, tipo, data_criacao, status, prazo, urgencia = tarefa
            print(f"ID: {id_tarefa} | Tipo: {tipo}")
            print(f"Descrição: {descricao}")
            print(f"Status: {status} | Urgência: {urgencia}")
            print(f"Data criação: {data_criacao.strftime('%Y-%m-%d %H:%M')}")
            if prazo:
                print(f"Prazo: {prazo}")
            print("-" * 50)
    except Error as e:
        print(f"Erro ao listar tarefas: {e}")
    finally:
        if cursor:
            cursor.close()
        conn.close()

def modificar_Tarefa(Tarefa_id, nova_descricao=None, novo_prazo=None, nova_urgencia=None):
    """
    Modifica uma Tarefa existente no banco de dados PostgreSQL.

    :param Tarefa_id: ID da Tarefa a ser modificada.
    :param nova_descricao: Nova descrição (opcional).
    :param novo_prazo: Novo prazo (opcional, formato YYYY-MM-DD).
    :param nova_urgencia: Nova urgência (opcional).
    """
    conn = criar_conexao()
    if conn is None:
        return
    
    cursor = None
    try:
        cursor = conn.cursor()
        updates = []
        params = []
        
        if nova_descricao:
            updates.append(sql.SQL("descricao = %s"))
            params.append(nova_descricao)
        if novo_prazo:
            updates.append(sql.SQL("prazo = %s"))
            params.append(novo_prazo)
        if nova_urgencia:
            updates.append(sql.SQL("urgencia = %s"))
            params.append(nova_urgencia)
        
        if not updates:
            print("Nenhuma modificação especificada.")
            return
        
        query = sql.SQL("UPDATE tarefas SET {} WHERE id = %s").format(
            sql.SQL(', ').join(updates)
        )
        params.append(Tarefa_id)
        cursor.execute(query, params)
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Tarefa ID {Tarefa_id} modificada com sucesso.")
        else:
            print(f"Tarefa ID {Tarefa_id} não encontrada.")
    except Error as e:
        print(f"Erro ao modificar tarefa: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        conn.close()

def marcar_Tarefa_concluida(Tarefa_id):
    """
    Marca uma Tarefa como concluída no banco de dados PostgreSQL.

    :param Tarefa_id: ID da Tarefa a ser marcada como concluída.
    """
    conn = criar_conexao()
    if conn is None:
        return
    
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE tarefas SET status = 'Concluída' WHERE id = %s", (Tarefa_id,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Tarefa ID {Tarefa_id} marcada como concluída.")
        else:
            print(f"Tarefa ID {Tarefa_id} não encontrada.")
    except Error as e:
        print(f"Erro ao marcar tarefa como concluída: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        conn.close()

def remover_Tarefa(Tarefa_id):
    """
    Remove uma Tarefa do banco de dados PostgreSQL.

    :param Tarefa_id: ID da Tarefa a ser removida.
    """
    conn = criar_conexao()
    if conn is None:
        return
    
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id = %s", (Tarefa_id,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Tarefa ID {Tarefa_id} removida.")
        else:
            print(f"Tarefa ID {Tarefa_id} não encontrada.")
    except Error as e:
        print(f"Erro ao remover tarefa: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        conn.close()
