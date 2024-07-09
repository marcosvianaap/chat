import threading
import socket
import signal
import sys

clients = []
usernames = {}
server_running = threading.Event()
server_running.set()

def handle_client(client, username):
    while server_running.is_set():
        try:
            msg = client.recv(2048)
            if not msg:
                remove_client(client, username)
                break
            broadcast(msg, username)
        except:
            remove_client(client, username)
            break

def broadcast(msg, sender):
    for client in clients:
        if usernames[client] != sender:
            try:
                client.send(msg)
            except:
                remove_client(client, usernames[client])

def remove_client(client, username):
    if client in clients:
        clients.remove(client)
        client.close()
        broadcast(f'{username} saiu do chat.'.encode('utf-8'), 'Servidor')

def signal_handler(sig, frame):
    print('\nEncerrando o servidor...')
    server_running.clear()
    for client in clients:
        try:
            client.close()
        except Exception as e:
            print(f'Erro ao fechar cliente: {e}')
    try:
        server.close()
    except Exception as e:
        print(f'Erro ao fechar servidor: {e}')

def main():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 7777)

    print("Iniciou o servidor de bate-papo")

    try:
        server.bind(server_address)
        server.listen()
    except Exception as e:
        print(f'\nNão foi possível iniciar o servidor! Erro: {e}\n')
        return

    signal.signal(signal.SIGINT, signal_handler)

    while server_running.is_set():
        try:
            server.settimeout(1.0)
            client, addr = server.accept()
            print(f'Cliente conectado com sucesso. IP: {addr}')

            client.send(''.encode('utf-8'))
            username = client.recv(2048).decode('utf-8')

            clients.append(client)
            usernames[client] = username

            print(f'Usuário {username} conectado.')
            broadcast(f'{username} entrou no chat.'.encode('utf-8'), 'Servidor')

            thread = threading.Thread(target=handle_client, args=(client, username))
            thread.start()
        except socket.timeout:
            continue
        except socket.error as e:
            print(f'Erro ao aceitar conexão: {e}')
            break

    print('Servidor encerrado.')

if __name__ == "__main__":
    main()



# hostname -I
# ifconfig
# ip addr show
