# QUESTÃO 2 - BIN PACKING
# Heurísticas Gulosas:
# 1. Next-Fit
# 2. First-Fit Decreasing


CAPACIDADE_SERVIDOR = 100

VMS_SOLICITADAS = [
48, 12, 35, 22, 17, 65, 8, 42, 53, 29,
14, 38, 47, 19, 25, 61, 33, 9, 55, 23,
44, 16, 50, 31, 11, 28, 58, 41, 13, 37,
62, 21, 45, 18, 26, 52, 34, 7, 49, 20,
39, 15, 57, 32, 12, 27, 54, 43, 10, 36,
60, 24, 46, 16, 22, 51, 30, 8, 40, 25
]


# NEXT-FIT


def next_fit(vms, capacidade):

    servidores = []

    servidor_atual = []
    uso_atual = 0

    for vm in vms:

        if uso_atual + vm <= capacidade:

            servidor_atual.append(vm)
            uso_atual += vm

        else:

            servidores.append(servidor_atual)

            servidor_atual = [vm]
            uso_atual = vm

    if servidor_atual:
        servidores.append(servidor_atual)

    return servidores



# FIRST-FIT DECREASING


def first_fit_decreasing(vms, capacidade):

    vms_ordenadas = sorted(vms, reverse=True)

    servidores = []

    for vm in vms_ordenadas:

        alocada = False

        for servidor in servidores:

            if sum(servidor) + vm <= capacidade:

                servidor.append(vm)
                alocada = True
                break

        if not alocada:

            servidores.append([vm])

    return servidores



# EXIBIÇÃO DOS RESULTADOS


def mostrar_servidores(nome, servidores):

    print(f"\n[{nome}]")
    print(f"Servidores utilizados: {len(servidores)}")

    for i, servidor in enumerate(servidores, start=1):

        total = sum(servidor)

        print(
            f"Servidor {i}: {servidor} "
            f"(Total: {total}/100 GB)"
        )



# PROGRAMA PRINCIPAL


def main():

    servidores_next_fit = next_fit(
        VMS_SOLICITADAS,
        CAPACIDADE_SERVIDOR
    )

    servidores_ffd = first_fit_decreasing(
        VMS_SOLICITADAS,
        CAPACIDADE_SERVIDOR
    )

    
    print("RESULTADO DA ALOCAÇÃO (HEURÍSTICAS)")
    

    mostrar_servidores(
        "Heurística Next-Fit",
        servidores_next_fit
    )

    mostrar_servidores(
        "Heurística First-Fit Decreasing",
        servidores_ffd
    )

    economia = (
        len(servidores_next_fit)
        - len(servidores_ffd)
    )

    
    print("CONCLUSÃO")
    

    print(
        f"A heurística First-Fit Decreasing "
        f"economizou {economia} servidor(es) "
        f"em relação à Next-Fit."
    )


if __name__ == "__main__":
    main()