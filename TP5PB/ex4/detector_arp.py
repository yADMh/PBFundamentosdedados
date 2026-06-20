from scapy.all import ARP, Ether, srp, sniff
from collections import defaultdict


# CONFIGURAÇÕES


REDE = "192.168.1.0/24"
IP_GATEWAY = "192.168.1.1"


# NETWORK SCANNER


def escanear_rede(rede):
    print(f"[*] Escaneando rede {rede}...")

    arp_request = ARP(pdst=rede)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")

    pacote = broadcast / arp_request

    respostas = srp(
        pacote,
        timeout=2,
        verbose=False
    )[0]

    tabela = {}

    print("\n[+] Dispositivos Encontrados:")
    print("-" * 50)

    for enviado, recebido in respostas:
        tabela[recebido.psrc] = recebido.hwsrc

        print(
            f"IP: {recebido.psrc:<15} "
            f"MAC: {recebido.hwsrc}"
        )

    return tabela



# DETECTOR DE ARP SPOOFING


def iniciar_monitoramento(
        tabela_verdade,
        gateway_ip):

    gateway_mac = tabela_verdade.get(gateway_ip)

    if not gateway_mac:
        print(
            f"\n[ERRO] Gateway "
            f"{gateway_ip} não encontrado."
        )
        return

    print("\n" + "=" * 60)
    print("[*] Iniciando monitoramento ARP...")
    print(f"[*] Gateway: {gateway_ip}")
    print(f"[*] MAC legítimo: {gateway_mac}")
    print("=" * 60)

    mac_para_ips = defaultdict(set)

    def analisar(pkt):

        if not pkt.haslayer(ARP):
            return

        arp = pkt[ARP]

        # Apenas respostas ARP
        if arp.op != 2:
            return

        ip_origem = arp.psrc
        mac_origem = arp.hwsrc

        mac_para_ips[mac_origem].add(ip_origem)

        
        # DETECÇÃO 1
        # Gateway com MAC alterado
        

        if ip_origem == gateway_ip:

            if mac_origem.lower() != gateway_mac.lower():

                print("\n[!!!] ALERTA DE MITM")
                print(
                    f"Gateway {gateway_ip}"
                )
                print(
                    f"MAC esperado: {gateway_mac}"
                )
                print(
                    f"MAC recebido: {mac_origem}"
                )

        
        # DETECÇÃO 2
        # Mesmo MAC para vários IPs
        

        if len(mac_para_ips[mac_origem]) > 2:

            print(
                "\n[!] Comportamento suspeito"
            )

            print(
                f"MAC: {mac_origem}"
            )

            print(
                "Respondendo pelos IPs:"
            )

            for ip in mac_para_ips[mac_origem]:
                print(f"   - {ip}")

    sniff(
        filter="arp",
        prn=analisar,
        store=False
    )



# MAIN


if __name__ == "__main__":

    tabela = escanear_rede(REDE)

    print("\n[+] Tabela da Verdade criada.")

    iniciar_monitoramento(
        tabela,
        IP_GATEWAY
    )

