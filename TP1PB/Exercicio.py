import datetime

Tarefas = []

# Função a ser chamada para adicionar uma peça a um computador ou modificar 
def adicionar_Tarefa(descricao, tipo="Nova", prazo=None, urgencia='Baixa'):
    """
    Adiciona uma nova Tarefa à lista.

    :param descricao: Descrição da Tarefa.
    :param tipo: Tipo (Nova Peça ou Modificação).
    :param prazo: Data de prazo final (opcional).
    :param urgencia: Nível de urgência (opcional, padrão é 'Baixa').
    """
    Tarefa = {
        'id': len(Tarefas) + 1,
        'descricao': descricao,
        'tipo': tipo,
        'data_criacao': datetime.datetime.now(),
        'status': 'Pendente',
        'prazo': prazo,
        'urgencia': urgencia
    }
    Tarefas.append(Tarefa)
    print(f"{tipo} adicionada: {descricao}")


# Função que lista as tarefas que já estão no sistema
def listar_Tarefas():
    """
    Lista todas as Tarefas.
    """
    if not Tarefas:
        print("Nenhuma Tarefa registrada.")
        return
    
    print("\n=== LISTA DE TAREFAS ===")
    for Tarefa in Tarefas:
        print(f"ID: {Tarefa['id']} | Tipo: {Tarefa['tipo']}")
        print(f"Descrição: {Tarefa['descricao']}")
        print(f"Status: {Tarefa['status']} | Urgência: {Tarefa['urgencia']}")
        print(f"Data criação: {Tarefa['data_criacao'].strftime('%Y-%m-%d %H:%M')}")
        if Tarefa['prazo']:
            print(f"Prazo: {Tarefa['prazo']}")
        print("-" * 50)

# Função para modificar as tarefas no sistama
def modificar_Tarefa(Tarefa_id, nova_descricao=None, novo_prazo=None, nova_urgencia=None):
    """
    Modifica uma Tarefa existente.

    :param Tarefa_id: ID da Tarefa a ser modificada.
    :param nova_descricao: Nova descrição (opcional).
    :param novo_prazo: Novo prazo (opcional).
    :param nova_urgencia: Nova urgência (opcional).
    """
    for Tarefa in Tarefas:
        if Tarefa['id'] == Tarefa_id:
            if nova_descricao:
                Tarefa['descricao'] = nova_descricao
            if novo_prazo:
                Tarefa['prazo'] = novo_prazo
            if nova_urgencia:
                Tarefa['urgencia'] = nova_urgencia
            print(f"Tarefa ID {Tarefa_id} modificada com sucesso.")
            return
    print(f"Tarefa ID {Tarefa_id} não encontrada.")

# Função de finalizar ou concluir a tarefa
def marcar_Tarefa_concluida(Tarefa_id):
    """
    Marca uma Tarefa como concluída.

    :param Tarefa_id: ID da Tarefa a ser marcada como concluída.
    """
    for Tarefa in Tarefas:
        if Tarefa['id'] == Tarefa_id:
            Tarefa['status'] = 'Concluída'
            print(f"Tarefa ID {Tarefa_id} marcada como concluída.")
            return
    print(f"Tarefa ID {Tarefa_id} não encontrada.")

# Função para remover uma tarefa simples
def remover_Tarefa(Tarefa_id):
    """
    Remove uma Tarefa da lista.

    :param Tarefa_id: ID da Tarefa a ser removida.
    """
    global Tarefas
    Tarefas = [Tarefa for Tarefa in Tarefas if Tarefa['id'] != Tarefa_id]
    print(f"Tarefa ID {Tarefa_id} removida.")

# Função para o menu de quando clica para adicionar a tarefa
def menu_adicionar():
    """
    Menu para adicionar nova Tarefa existente.
    """
    print("\n=== ADICIONAR NOVA TAREFA ===")
    print("1. Adicionar Nova Tarefa")
    print("2. Modificar em Tarefa Existente")
    print("3. Voltar ao menu principal")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == '1':
        descricao = input("Descrição da nova Tarefa: ")
        prazo = input("Prazo (YYYY-MM-DD) ou deixe em branco: ")
        urgencia = input("Urgência (Baixa, Média, Alta): ")
        adicionar_Tarefa(descricao, "Nova Tarefa", prazo if prazo else None, urgencia if urgencia else 'Baixa')
    
    elif opcao == '2':
        descricao = input("Descrição da modificação: ")
        prazo = input("Prazo (YYYY-MM-DD) ou deixe em branco: ")
        urgencia = input("Urgência (Baixa, Média, Alta): ")
        adicionar_Tarefa(descricao, "Modificação", prazo if prazo else None, urgencia if urgencia else 'Baixa')
    
    elif opcao == '3':
        return
    
    else:
        print("Opção inválida.")

# Função do menu(começo)
def menu():
    """
    Menu principal do sistema.
    """
    while True:
        print("\n=== SISTEMA DE GESTÃO DE MONTAGEM DE COMPUTADOR ===")
        print("1. Adicionar Nova Tarefa")
        print("2. Listar Todas as Tarefas")
        print("3. Modificar Tarefa Existente")
        print("4. Marcar como Concluída")
        print("5. Remover Tarefa")
        print("6. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            menu_adicionar()
        elif opcao == '2':
            listar_Tarefas()
        elif opcao == '3':
            Tarefa_id = int(input("ID da Tarefa a ser modificada: "))
            nova_descricao = input("Nova descrição (deixe em branco para não alterar): ")
            novo_prazo = input("Novo prazo (YYYY-MM-DD) ou deixe em branco: ")
            nova_urgencia = input("Nova urgência (Baixa, Média, Alta) ou deixe em branco: ")
            modificar_Tarefa(Tarefa_id, 
                          nova_descricao if nova_descricao else None, 
                          novo_prazo if novo_prazo else None, 
                          nova_urgencia if nova_urgencia else None)
        elif opcao == '4':
            Tarefa_id = int(input("ID da Tarefa a ser marcada como concluída: "))
            marcar_Tarefa_concluida(Tarefa_id)
        elif opcao == '5':
            Tarefa_id = int(input("ID da Tarefa a ser removida: "))
            remover_Tarefa(Tarefa_id)
        elif opcao == '6':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Iniciar o sistema
print("Bem-vindo ao Sistema de Gestão de Montagem de Computador!")
menu()
