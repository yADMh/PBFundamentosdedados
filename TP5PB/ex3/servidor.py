import socket
import ssl

HOST = "127.0.0.1"
PORT = 8443

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    certfile="cert.pem",
    keyfile="key.pem"
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)

    print(f"[Servidor] Escutando em {HOST}:{PORT}")

    with context.wrap_socket(sock, server_side=True) as tls_sock:

        conn, addr = tls_sock.accept()

        print(f"[Servidor] Conexão TLS recebida de {addr}")

        data = conn.recv(4096)

        if data:
            mensagem = data.decode("utf-8")
            print(
                f"[Servidor] Comando Seguro Recebido: {mensagem}"
            )

        conn.close()