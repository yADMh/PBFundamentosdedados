# Questão 5 - Recon Automation
## Automatização de Reconhecimento de Superfície de Ataque (DNS + Nmap)

## Visão Geral

Este projeto implementa uma ferramenta de reconhecimento automatizado (Black Box Reconnaissance) voltada para análise de superfície de ataque externa.

O sistema integra duas ferramentas amplamente utilizadas em auditoria de segurança:

- DNSRecon → Enumeração de DNS e descoberta de subdomínios  
- Nmap (python-nmap) → Varredura de portas e identificação de serviços  

O objetivo é simular o fluxo inicial de um teste de invasão profissional, onde o analista precisa mapear completamente um alvo antes de qualquer exploração.

---

## Objetivo da Questão

A ferramenta deve automatizar:

- Coleta de registros DNS do alvo  
- Descoberta de subdomínios via brute force  
- Extração de endereços IP a partir dos resultados DNS  
- Varredura de serviços e portas abertas com Nmap  
- Geração de relatório estruturado em JSON e saída no terminal  

---

## Funcionalidades Implementadas

### 1. Módulo DNSRecon

A função `executar_dnsrecon()` realiza:

Enumeração de registros DNS:
- A
- AAAA
- MX
- NS
- TXT (dependendo da resposta do servidor)

Execução via subprocess:
dnsrecon -d zonetransfer.me -t std

Saída processada:
- Lista de registros DNS
- Filtro de servidores MX
- Identificação de subdomínios do tipo [A]

---

### 2. Brute Force de Subdomínios

A função `brute_force_subdominios()`:

Usa wordlist:
subdomains-top1mil-5000.txt

Executa:
dnsrecon -d alvo -D wordlist -t brt

Filtra apenas entradas válidas [A]

Resultado:
Lista de subdomínios encontrados (quando existem respostas válidas).

---

### 3. Extração de Hosts (IP Resolver)

Função: `extrair_hosts()`

O que faz:
- Usa regex para extrair IPs dos resultados DNS
- Remove duplicatas com set()
- Retorna lista de alvos para o Nmap

Exemplo:
192.168.1.1  
142.250.102.26  
5.196.105.14  

---

### 4. Varredura com Nmap (python-nmap)

Função: `executar_nmap()`

Configuração do scan:
-Pn -F -sV --script=discovery

Significado:
- -Pn → ignora ping
- -F → fast scan
- -sV → detecção de versão
- --script=discovery → scripts NSE

Dados coletados:
- Estado do host
- Protocolos
- Portas abertas
- Serviços
- Versões

---

### 5. Geração de Relatório

Função: `salvar_relatorio()`

Arquivo gerado:
relatorio_recon.json

Contém:
- Data da execução
- DNS completo
- Brute force DNS
- Hosts extraídos
- Resultado do Nmap

---

### 6. Saída no Terminal

RELATÓRIO AUTOMATIZADO DE SUPERFÍCIE DE ATAQUE

[+] Alvo analisado: zonetransfer.me

[1] RESULTADOS DNS
- MX Google Mail Servers
- Registros A e NS

Subdomínios encontrados:
* (caso existam)

[2] RESULTADOS NMAP
--------------------------------
Host: 142.250.102.26
--------------------------------
Porta 80/tcp | open | http
Porta 443/tcp | open | https

[+] Relatório salvo em: relatorio_recon.json

---

## Execução do Projeto

### 1. Instalar dependências
pip install python-nmap  
sudo apt install dnsrecon nmap  

### 2. Executar o script
sudo python3 recon_automation.py  

---

## Fluxo de Execução

DNSRecon  
↓  
Brute Force DNS  
↓  
Extração de IPs  
↓  
Nmap Scan  
↓  
Relatório JSON + Output terminal  

---

## Exemplo de Arquivo Gerado

{
  "data": "2026-06-20 04:47:57",
  "dns": {},
  "dns_bruteforce": [],
  "nmap": {}
}

---

## Observações Importantes

✔ Uso ético  
Somente em ambientes autorizados e laboratórios.

✔ Limitações  
- Scan rápido (-F)
- NSE em modo discovery
- Sem exploração ativa

✔ Requisitos  
- sudo/root
- dnsrecon
- nmap
- python-nmap

---

## Conclusão

Ferramenta de recon automatizado que integra DNS + Nmap para simular um fluxo real de análise de superfície de ataque (Black Box Recon).
