# Questão 2 - Bin Packing Problem - Heurísticas de Alocação de VMs

## Visão Geral

Este projeto implementa a resolução do **Problema do Empacotamento (Bin Packing Problem)** aplicado à alocação de Máquinas Virtuais (VMs) em servidores físicos.

Cada servidor possui capacidade fixa de **100 GB de RAM**, e o objetivo é minimizar a quantidade de servidores utilizados para comportar todas as VMs solicitadas.

Foram aplicadas duas heurísticas gulosas:

- Next-Fit (Próximo Encaixe)
- First-Fit Decreasing (Primeiro Encaixe Decrescente)

---

## Tecnologias Utilizadas

- Python 3
- Terminal Linux
- Algoritmos Gulosos (Greedy Algorithms)

---

## Entrada do Problema

CAPACIDADE_SERVIDOR = 100 GB

VMS_SOLICITADAS = [48, 12, 35, 22, 17, 65, 8, 42, 53, 29,
14, 38, 47, 19, 25, 61, 33, 9, 55, 23,
44, 16, 50, 31, 11, 28, 58, 41, 13, 37,
62, 21, 45, 18, 26, 52, 34, 7, 49, 20,
39, 15, 57, 32, 12, 27, 54, 43, 10, 36,
60, 24, 46, 16, 22, 51, 30, 8, 40, 25]

---

## Heurísticas Implementadas

### Next-Fit
- Mantém apenas um servidor aberto por vez
- Se não couber, abre outro servidor
- Não revisita servidores anteriores

### First-Fit Decreasing
- Ordena VMs em ordem decrescente
- Tenta alocar no primeiro servidor disponível
- Mais eficiente em média

---

## Resultados da Execução

### Next-Fit
- Servidores utilizados: 24

### First-Fit Decreasing
- Servidores utilizados: 20

Economia de 4 servidores

---

## Como Executar

python3 bin_packing.py
