import datetime


tarefas = []


def adicionar_tarefa(descricao, prazo=None, urgencia='Baixa'):
    """
    Adiciona uma nova tarefa à lista de tarefas.

    :param descricao: Descrição da tarefa.
    :param prazo: Data de prazo final da tarefa (opcional).
    :param urgencia: Nível de urgência da tarefa (opcional, padrão é 'Baixa').
    """
    tarefa = {
        'id': len(tarefas) + 1,
        'descricao': descricao,
        'data_criacao': datetime.datetime.now(),
        'status': 'Pendente',
        'prazo': prazo,
        'urgencia': urgencia
    }
    tarefas.append(tarefa)
    print(f"Tarefa adicionada: {tarefa}")


def listar_tarefas():
    """
    Lista todas as tarefas pendentes.
    """
    if not tarefas:
        print("Nenhuma tarefa pendente.")
        return
    for tarefa in tarefas:
        print(f"ID: {tarefa['id']}, Descrição: {tarefa['descricao']}, "
              f"Status: {tarefa['status']}, Prazo: {tarefa['prazo']}, "
              f"Urgência: {tarefa['urgencia']}")
        

def marcar_tarefa_concluida(tarefa_id):
    """
    Marca uma tarefa como concluída.

    :param tarefa_id: ID da tarefa a ser marcada como concluída.
    """
    for tarefa in tarefas:
        if tarefa['id'] == tarefa_id:
            tarefa['status'] = 'Concluída'
            print(f"Tarefa ID {tarefa_id} marcada como concluída.")
            return
    print(f"Tarefa ID {tarefa_id} não encontrada.")


def remover_tarefa(tarefa_id):
    """
    Remove uma tarefa da lista.

    :param tarefa_id: ID da tarefa a ser removida.
    """
    global tarefas
    tarefas = [tarefa for tarefa in tarefas if tarefa['id'] != tarefa_id]
    print(f"Tarefa ID {tarefa_id} removida.")
    

def menu():
    """
    Exibe o menu de opções e processa a escolha do usuário.
    """
    while True:
        print("\nMenu de Gestão de Tarefas:")
        print("1. Adicionar Tarefa")
        print("2. Listar Tarefas")
        print("3. Marcar Tarefa como Concluída")
        print("4. Remover Tarefa")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            descricao = input("Descrição da tarefa: ")
            prazo = input("Prazo (YYYY-MM-DD) ou deixe em branco: ")
            urgencia = input("Urgência (Baixa, Média, Alta): ")
            adicionar_tarefa(descricao, prazo if prazo else None, urgencia if urgencia else 'Baixa')
        elif opcao == '2':
            listar_tarefas()
        elif opcao == '3':
            tarefa_id = int(input("ID da tarefa a ser marcada como concluída: "))
            marcar_tarefa_concluida(tarefa_id)
        elif opcao == '4':
            tarefa_id = int(input("ID da tarefa a ser removida: "))
            remover_tarefa(tarefa_id)
        elif opcao == '5':
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")


menu()