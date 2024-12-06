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

client_games = {}

while True:
    msg, sender_addr_port = sock.recvfrom(2048)
    msg_decoded = msg.decode().strip()
    print('Mensagem de {}:{} -> {}'.format(sender_addr_port[0], sender_addr_port[1], msg_decoded))

    if msg_decoded == "game":
        if sender_addr_port not in client_games:
            server_choice = random.randint(1, 100)
            client_games[sender_addr_port] = {
                "server_choice": server_choice,
                "attempts": 0
            }
            print(f"Novo jogo para o cliente {sender_addr_port}")
            print(f"Número gerado: {server_choice}")

        msg = "Bem-Vindo ao jogo!\nTenta adivinhar um número entre 1 e 100.".encode()
        sock.sendto(msg, sender_addr_port)

    elif sender_addr_port in client_games:
        game = client_games[sender_addr_port]
        try:
            client_choice = int(msg_decoded)

            if client_choice > game["server_choice"]:
                msg = "Valor muito alto, tenta um mais baixo!".encode()
                game["attempts"] += 1
            elif client_choice < game["server_choice"]:
                msg = "Valor muito baixo, tenta um mais alto!".encode()
                game["attempts"] += 1
            else:
                game["attempts"] += 1
                msg = f"Parabéns! Conseguiste acertar, com {game['attempts']} tentativa(s).\nO valor era: {game['server_choice']}.".encode()
                del client_games[sender_addr_port]

        except ValueError:
            msg = "Por favor, introduz um número válido entre 1 e 100.".encode()

        sock.sendto(msg, sender_addr_port)

    else:
        echo_msg = f"ECHO: {msg_decoded}".encode()
        sock.sendto(echo_msg, sender_addr_port)