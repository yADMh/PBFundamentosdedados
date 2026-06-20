import subprocess
import json
import re
import nmap
from datetime import datetime

ALVO = "zonetransfer.me"
ARQUIVO_RELATORIO = "relatorio_recon.json"


def executar_dnsrecon(alvo):
    resultado = {
        "registros": [],
        "subdominios": []
    }

    try:
        print("[*] Executando DNSRecon...")

        comando = [
            "dnsrecon",
            "-d", alvo,
            "-t", "std"
        ]

        saida = subprocess.run(
            comando,
            capture_output=True,
            text=True
        )

        resultado["registros"] = saida.stdout.splitlines()

        for linha in saida.stdout.splitlines():

            if "MX" in linha:
                resultado.setdefault("mx", []).append(linha)

            if "[A]" in linha:
                resultado["subdominios"].append(linha)

        return resultado

    except Exception as erro:
        return {"erro": str(erro)}


def brute_force_subdominios(alvo):
    try:

        print("[*] Executando brute force DNS...")

        comando = [
            "dnsrecon",
            "-d", alvo,
            "-D", "subdomains-top1mil-5000.txt",
            "-t", "brt"
        ]

        saida = subprocess.run(
            comando,
            capture_output=True,
            text=True
        )

        encontrados = []

        for linha in saida.stdout.splitlines():

            if "[A]" in linha:
                encontrados.append(linha)

        return encontrados

    except Exception as erro:
        return [f"Erro: {erro}"]


def extrair_hosts(dados_dns):

    hosts = set()

    padrao_ip = r"(\d+\.\d+\.\d+\.\d+)"

    for linha in dados_dns:

        match = re.search(padrao_ip, linha)

        if match:
            hosts.add(match.group(1))

    return list(hosts)


def executar_nmap(alvos):

    scanner = nmap.PortScanner()

    resultados = {}

    for host in alvos:

        print(f"[*] Escaneando {host}")

        try:

            scanner.scan(
                hosts=host,
                arguments="-Pn -F -sV --script=discovery --host-timeout 30s"
                )

            host_info = {}

            if host in scanner.all_hosts():

                host_info["estado"] = scanner[host].state()
                host_info["protocolos"] = {}

                for proto in scanner[host].all_protocols():

                    host_info["protocolos"][proto] = []

                    for porta in scanner[host][proto]:

                        servico = scanner[host][proto][porta]

                        host_info["protocolos"][proto].append({
                            "porta": porta,
                            "estado": servico.get("state"),
                            "servico": servico.get("name"),
                            "versao": servico.get("product"),
                            "extra": servico.get("version")
                        })

            resultados[host] = host_info

        except Exception as erro:

            resultados[host] = {
                "erro": str(erro)
            }

    return resultados


def salvar_relatorio(relatorio):

    with open(
        ARQUIVO_RELATORIO,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            relatorio,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


def imprimir_resumo(relatorio):

    
    print("RELATÓRIO AUTOMATIZADO DE SUPERFÍCIE DE ATAQUE")
   

    print(f"\n[+] Alvo analisado: {ALVO}")

    print("\n[1] RESULTADOS DNS")

    for item in relatorio["dns"].get("mx", []):
        print("-", item)

    print("\nSubdomínios encontrados:")

    for sub in relatorio["dns_bruteforce"]:
        print("*", sub)

    print("\n[2] RESULTADOS NMAP")

    for host, info in relatorio["nmap"].items():

        print("\n--------------------------------")
        print(f"Host: {host}")
        print("--------------------------------")

        protocolos = info.get("protocolos", {})

        for proto, portas in protocolos.items():

            for porta in portas:

                print(
                    f"Porta {porta['porta']}/{proto}"
                    f" | {porta['estado']}"
                    f" | {porta['servico']}"
                    f" {porta['versao'] or ''}"
                )

    print(
        f"\n[+] Relatório salvo em: "
        f"{ARQUIVO_RELATORIO}"
    )


if __name__ == "__main__":

    relatorio = {
        "data": str(datetime.now())
    }

    dns = executar_dnsrecon(ALVO)

    brute = brute_force_subdominios(ALVO)

    hosts = extrair_hosts(
    dns.get("registros", [])
    )[:3]

    nmap_resultado = executar_nmap(hosts)

    relatorio["dns"] = dns
    relatorio["dns_bruteforce"] = brute
    relatorio["nmap"] = nmap_resultado

    salvar_relatorio(relatorio)

    imprimir_resumo(relatorio)
