# Questão 4 – Detector de Ataque Man-in-the-Middle (ARP Spoofing)

## Objetivo

O objetivo deste exercício é desenvolver uma ferramenta de monitoramento de rede capaz de:

1. Descobrir os dispositivos ativos da rede local.
2. Criar uma tabela confiável contendo os endereços IP e MAC dos hosts encontrados.
3. Monitorar o tráfego ARP em tempo real.
4. Detectar possíveis ataques de ARP Spoofing utilizados em ataques Man-in-the-Middle (MitM).

Para a implementação foi utilizada a biblioteca **Scapy**, amplamente utilizada em testes de segurança e análise de protocolos de rede.

---

# Tecnologias Utilizadas

- Python 3
- Scapy
- ARP (Address Resolution Protocol)
- Linux Ubuntu
- VirtualBox

---

# Cenário

A empresa relatou lentidão na rede e suspeitas de que um invasor esteja tentando interceptar credenciais dos usuários através de um ataque de Man-in-the-Middle.

Antes de detectar um ataque, é necessário conhecer a estrutura legítima da rede.

Por esse motivo a aplicação foi dividida em duas etapas:

- Network Scanner
- Detector de ARP Spoofing

---

# Parte 1 – Network Scanner

## Objetivo

Descobrir os dispositivos ativos na rede local através do envio de pacotes ARP Request.

O scanner envia uma solicitação para todos os endereços IP da rede configurada.

Hosts ativos respondem informando:

- Endereço IP
- Endereço MAC

Essas informações são utilizadas para criar a chamada:

```text
Tabela da Verdade
```

que representa o estado legítimo da rede.

---

## Configuração Utilizada

Rede identificada na máquina virtual:

```text
10.0.2.0/24
```

Gateway identificado:

```text
10.0.2.2
```

---

## Resultado Obtido

Durante a execução foram encontrados os seguintes dispositivos:

```text
[*] Escaneando rede 10.0.2.0/24...

[+] Dispositivos Encontrados:
--------------------------------------------------
IP: 10.0.2.2        MAC: 52:55:0a:00:02:02
IP: 10.0.2.3        MAC: 52:55:0a:00:02:03

[+] Tabela da Verdade criada.
```

---

## Tabela da Verdade

| IP | MAC |
|-----|-----|
| 10.0.2.2 | 52:55:0a:00:02:02 |
| 10.0.2.3 | 52:55:0a:00:02:03 |

O gateway legítimo identificado foi:

```text
10.0.2.2
```

com endereço MAC:

```text
52:55:0a:00:02:02
```

---

# Parte 2 – Detector de ARP Spoofing

## Objetivo

Após criar a tabela confiável da rede, o sistema entra em modo de monitoramento contínuo.

O programa captura apenas pacotes ARP através do filtro:

```python
filter="arp"
```

e analisa todas as respostas ARP recebidas.

---

# Critérios de Detecção

## Detecção 1 – Gateway com MAC Alterado

O sistema compara cada resposta ARP recebida com o endereço MAC legítimo do gateway.

Exemplo de comportamento suspeito:

```text
Gateway: 10.0.2.2

MAC esperado:
52:55:0a:00:02:02

MAC recebido:
AA:BB:CC:DD:EE:FF
```

Neste cenário o programa gera um alerta indicando possível tentativa de ARP Spoofing.

Exemplo:

```text
[!!!] ALERTA DE MITM

Gateway 10.0.2.2

MAC esperado:
52:55:0a:00:02:02

MAC recebido:
AA:BB:CC:DD:EE:FF
```

---

## Detecção 2 – Mesmo MAC Respondendo por Múltiplos IPs

Outra característica comum de ataques MitM é quando um único equipamento começa a responder por vários endereços IP da rede.

Exemplo:

```text
MAC:
AA:BB:CC:DD:EE:FF

Respondendo pelos IPs:

10.0.2.2
10.0.2.15
10.0.2.20
```

Neste caso o programa também gera um alerta.

Exemplo:

```text
[!] Comportamento suspeito

MAC:
AA:BB:CC:DD:EE:FF

Respondendo pelos IPs:
 - 10.0.2.2
 - 10.0.2.15
 - 10.0.2.20
```

---

# Execução

## Instalação da Biblioteca

```bash
pip install scapy
```

---

## Execução do Programa

Necessário executar com privilégios administrativos:

```bash
sudo python3 detector_arp.py
```

---

## Resultado Obtido

Durante os testes o programa identificou corretamente o gateway legítimo da rede:

```text
============================================================
[*] Iniciando monitoramento ARP...
[*] Gateway: 10.0.2.2
[*] MAC legítimo: 52:55:0a:00:02:02
============================================================
```

Nenhuma alteração suspeita foi detectada durante o período de monitoramento.

Isso indica que:

- Não houve alteração do MAC do gateway.
- Nenhum host respondeu por múltiplos IPs de forma anormal.
- Não foram encontrados indícios de ARP Spoofing.

---

# Conclusão

O objetivo do exercício foi alcançado com sucesso.

A ferramenta desenvolvida foi capaz de:

- Descobrir dispositivos ativos na rede.
- Associar corretamente endereços IP e MAC.
- Criar uma tabela de referência confiável.
- Monitorar pacotes ARP em tempo real.
- Detectar alterações suspeitas relacionadas a ataques Man-in-the-Middle.

A solução demonstra uma técnica amplamente utilizada em ambientes corporativos para identificar tentativas de interceptação de tráfego através de ARP Spoofing.