from tasks import adicionar_Tarefa, listar_Tarefas, modificar_Tarefa, marcar_Tarefa_concluida, remover_Tarefa

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
        prazo = input("Prazo (YYYY-MM-DD) ou deixe em branco: ").strip()
        urgencia = input("Urgência (Baixa, Média, Alta): ").strip() or 'Baixa'
        adicionar_Tarefa(descricao, "Nova Tarefa", prazo if prazo else None, urgencia)
    
    elif opcao == '2':
        descricao = input("Descrição da modificação: ")
        prazo = input("Prazo (YYYY-MM-DD) ou deixe em branco: ").strip()
        urgencia = input("Urgência (Baixa, Média, Alta): ").strip() or 'Baixa'
        adicionar_Tarefa(descricao, "Modificação", prazo if prazo else None, urgencia)
    
    elif opcao == '3':
        return
    
    else:
        print("Opção inválida.")

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
            try:
                Tarefa_id = int(input("ID da Tarefa a ser modificada: "))
                nova_descricao = input("Nova descrição (deixe em branco para não alterar): ").strip()
                novo_prazo = input("Novo prazo (YYYY-MM-DD) ou deixe em branco: ").strip()
                nova_urgencia = input("Nova urgência (Baixa, Média, Alta) ou deixe em branco: ").strip()
                modificar_Tarefa(Tarefa_id, 
                              nova_descricao if nova_descricao else None, 
                              novo_prazo if novo_prazo else None, 
                              nova_urgencia if nova_urgencia else None)
            except ValueError:
                print("ID deve ser um número inteiro válido.")
        elif opcao == '4':
            try:
                Tarefa_id = int(input("ID da Tarefa a ser marcada como concluída: "))
                marcar_Tarefa_concluida(Tarefa_id)
            except ValueError:
                print("ID deve ser um número inteiro válido.")
        elif opcao == '5':
            try:
                Tarefa_id = int(input("ID da Tarefa a ser removida: "))
                remover_Tarefa(Tarefa_id)
            except ValueError:
                print("ID deve ser um número inteiro válido.")
        elif opcao == '6':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")
