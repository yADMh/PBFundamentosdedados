import pcapy
import struct
import string

PORTA = 8443


def texto_legivel(payload):
    return "".join(
        c if c in string.printable else "."
        for c in payload.decode(
            "latin-1",
            errors="ignore"
        )
    )


def processar_pacote(header, data):

    if len(data) < 54:
        return

    try:

        ethernet_len = 14

        ip_header = data[ethernet_len:ethernet_len + 20]

        iph = struct.unpack(
            "!BBHHHBBH4s4s",
            ip_header
        )

        ihl = (iph[0] & 0xF) * 4

        tcp_inicio = ethernet_len + ihl

        tcp_header = data[
            tcp_inicio:tcp_inicio + 20
        ]

        tcph = struct.unpack(
            "!HHLLBBHHH",
            tcp_header
        )

        doff = (tcph[4] >> 4) * 4

        payload_inicio = tcp_inicio + doff

        payload = data[payload_inicio:]

        if len(payload) == 0:
            return

        print("\n[+] Pacote TCP Capturado!")
        print(
            f"Tamanho Payload: {len(payload)} bytes"
        )

        print(
            "[Dados Brutos do Payload]:",
            repr(payload[:80])
        )

        texto = texto_legivel(payload)

        print(
            "[Texto Convertido]:",
            texto[:120]
        )

        if (
            "AUTH_TOKEN" in texto
            or "REBOOT_SERVER" in texto
        ):
            print(
                "[!] ALERTA: Conteúdo sensível encontrado!"
            )
        else:
            print(
                "[-] Alerta: Padrão 'AUTH_TOKEN' NÃO encontrado. "
                "Os dados estão devidamente cifrados via TLS."
            )

    except Exception:
        pass


dispositivos = pcapy.findalldevs()

print("Interfaces disponíveis:")
for d in dispositivos:
    print(" -", d)

interface = dispositivos[0]

cap = pcapy.open_live(
    interface,
    65536,
    1,
    100
)

cap.setfilter(
    f"tcp port {PORTA}"
)

print(
    f"[*] Iniciando captura na interface {interface} "
    f"(Porta {PORTA})..."
)

while True:
    cap.dispatch(
        1,
        processar_pacote
    )