import socket
import signal
import sys
import time

def signal_handler(sig, frame):
    print()
    message = "A sair"
    for i in range(4):
        sys.stdout.write("\r" + message + "." * i)
        sys.stdout.flush()
        time.sleep(0.5)
    print()
    sys.exit(0)

if (len(sys.argv) <= 1):
    print("Usage: python(3) client.py <IP>")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')

ip_addr = sys.argv[1]
udp_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

try:
    sock.sendto("ping".encode(), (ip_addr, udp_port))
    data, addr = sock.recvfrom(2048)
    if data.decode() == "pong":
        print("Conexão com o servidor bem-sucedida!")
except socket.timeout:
    print("Não foi possível conectar ao servidor")
    sys.exit(1)

while True:
    try:
        try:
            data, addr = sock.recvfrom(2048)
            print(data.decode())
        except socket.timeout:
            print("Nenhuma resposta do servidor.")

        message = input("Mensagem para enviar? ").encode()
        if message == "exit".encode() or message == "sair".encode() or message == "sair".encode():
            message = "A sair"
            for i in range(4):
                sys.stdout.write("\r" + message + "." * i)
                sys.stdout.flush()
                time.sleep(0.5)
            print()
            sys.exit(0)
        if len(message) > 0:
            sock.sendto(message, (ip_addr, udp_port))


    except KeyboardInterrupt:
        break