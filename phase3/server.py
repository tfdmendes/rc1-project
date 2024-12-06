import socket
import signal
import sys
import random

def signal_handler(sig, frame):
    print('\nServidor encerrado!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Pressione Ctrl+C para sair...')

ip_addr = "0.0.0.0"
udp_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip_addr, udp_port))

print(f"Servidor UDP iniciado em {ip_addr}:{udp_port}")

while True:
    message, sender_addr_port = sock.recvfrom(2048)
    print('Mensagem de {}:{} -> {}'.format(sender_addr_port[0], sender_addr_port[1], message.decode()))

    if message.decode() == "game":
        msg = ("Bem-Vindo ao jogo!\nO objetivo é adivinhares um número entre 1 e 100.").encode()
        sock.sendto(msg, (sender_addr_port[0], sender_addr_port[1]))

        server_choice = random.randint(1, 100)
        print(f"Número gerado pelo servidor: {server_choice}")
        attempt = 0

        while True:
            try:
                request, sender_addr_port = sock.recvfrom(2048)
                client_choice = int(request.decode().strip())

                if client_choice > server_choice:
                    msg = "Valor muito alto, tenta um mais baixo!".encode()
                    attempt += 1
                elif client_choice < server_choice:
                    msg = "Valor muito baixo, tenta um mais alto!".encode()
                    attempt += 1
                else:
                    attempt += 1
                    msg = f"Parabéns! Conseguiste acertar, com {attempt} tentativa(s).\nO valor era: {server_choice}.".encode()
                    sock.sendto(msg, (sender_addr_port[0], sender_addr_port[1]))
                    break
            except ValueError:
                msg = "Por favor, introduz um número válido entre 1 e 100.".encode()

            sock.sendto(msg, (sender_addr_port[0], sender_addr_port[1]))
    else:
        sock.sendto(("ECHO: " + message.decode()).encode(), (sender_addr_port[0], sender_addr_port[1]))