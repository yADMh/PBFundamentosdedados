# Questão 1 - REDE DE FIBRA ÓTICA — KRUSKAL + DIJKSTRA

## Visão Geral

Este projeto simula o planejamento de uma rede de fibra ótica entre 30 cidades interconectadas, com o objetivo de resolver dois problemas clássicos de grafos:

- Construir uma rede de menor custo possível sem ciclos
- Calcular a latência mínima acumulada a partir da cidade 0 até todas as outras cidades

Para isso, foram implementados manualmente os algoritmos de:

- Algoritmo de Kruskal (Árvore Geradora Mínima)
- Algoritmo de Dijkstra (Menor caminho em grafos ponderados)
- Estrutura Union-Find (conjuntos disjuntos)

---

## Problema

Uma empresa de telecomunicações precisa:

### 1. Etapa de Infraestrutura
Construir uma rede conectando todas as cidades com o menor custo total possível, evitando ciclos.

### 2. Etapa de Operação
Calcular a menor latência acumulada da cidade 0 até todas as demais cidades usando todas as conexões disponíveis.

---

## Modelagem do Problema

Cada conexão é representada por:

(origem, destino, custo, latência)

Exemplo:
(0, 1, 45, 3)

---

## Algoritmos Utilizados

### Kruskal (MST)

- Ordena arestas por custo
- Evita ciclos
- Usa Union-Find

### Dijkstra

- Calcula menor caminho da cidade 0
- Usa latência como peso

---

## Saída do Programa

### Rede de menor custo
Cidade A <-> Cidade B | Custo: X

### Custo total
Custo Total da Rede: 1065

### Latência acumulada
Cidade 0: 0 ms
Cidade 1: 3 ms
...

---

## Execução

python3 fibra_otica.py

---

## Complexidade

Kruskal: O(E log E)  
Dijkstra: O(N²)

---

## Conclusão

O sistema otimiza:

- Custo de implantação da rede
- Latência de comunicação
