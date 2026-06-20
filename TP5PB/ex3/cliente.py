import socket
import ssl

HOST = "127.0.0.1"
PORT = 8443

mensagem = "AUTH_TOKEN:XYZ123:CMD:REBOOT_SERVER"

context = ssl.create_default_context()

context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

with socket.create_connection((HOST, PORT)) as sock:

    with context.wrap_socket(
        sock,
        server_hostname=HOST
    ) as tls_sock:

        tls_sock.sendall(
            mensagem.encode("utf-8")
        )

        print(
            f"[Cliente] Mensagem enviada: {mensagem}"
        )