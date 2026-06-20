CAPACIDADE_SERVIDOR = 100  # GB

VMS_SOLICITADAS = [
    48, 12, 35, 22, 17, 65, 8, 42, 53, 29,
    14, 38, 47, 19, 25, 61, 33, 9, 55, 23,
    44, 16, 50, 31, 11, 28, 58, 41, 13, 37,
    62, 21, 45, 18, 26, 52, 34, 7, 49, 20,
    39, 15, 57, 32, 12, 27, 54, 43, 10, 36,
    60, 24, 46, 16, 22, 51, 30, 8, 40, 25
]



# NEXT-FIT

def next_fit(vms):
    servidores = []
    servidor_atual = []
    uso_atual = 0

    for vm in vms:
        if uso_atual + vm <= CAPACIDADE_SERVIDOR:
            servidor_atual.append(vm)
            uso_atual += vm
        else:
            servidores.append((servidor_atual, uso_atual))
            servidor_atual = [vm]
            uso_atual = vm

    if servidor_atual:
        servidores.append((servidor_atual, uso_atual))

    return servidores



# FIRST-FIT DECREASING

def first_fit_decreasing(vms):
    vms_ordenadas = sorted(vms, reverse=True)

    servidores = []  # cada servidor: [lista_vms, uso]

    for vm in vms_ordenadas:
        colocado = False

        for i in range(len(servidores)):
            vms_srv, uso = servidores[i]

            if uso + vm <= CAPACIDADE_SERVIDOR:
                vms_srv.append(vm)
                servidores[i] = (vms_srv, uso + vm)
                colocado = True
                break

        if not colocado:
            servidores.append(([vm], vm))

    return servidores



# RELATÓRIO

def imprimir_relatorio(nome, servidores):
    print(f"\n[{nome}]")
    print(f"- Servidores utilizados: {len(servidores)}")

    for i, (vms, uso) in enumerate(servidores[:3], start=1):
        print(f"- Exemplo Servidor {i}: {vms} (Total: {uso}/100 GB)")


def main():
    nf = next_fit(VMS_SOLICITADAS)
    ffd = first_fit_decreasing(VMS_SOLICITADAS)

    print("=== RESULTADO DA ALOCAÇÃO (HEURÍSTICAS) ===")

    imprimir_relatorio("Heurística Next-Fit", nf)
    imprimir_relatorio("Heurística First-Fit Decreasing", ffd)

    diff = len(nf) - len(ffd)

    print("\nConclusão:")
    if diff > 0:
        print(f"First-Fit Decreasing economizou {diff} servidores em relação ao Next-Fit.")
    elif diff < 0:
        print(f"Next-Fit economizou {-diff} servidores em relação ao First-Fit Decreasing.")
    else:
        print("Ambas heurísticas utilizaram a mesma quantidade de servidores.")


if __name__ == "__main__":
    main()