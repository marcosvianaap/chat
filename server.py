import threading
import socket

clients = []
usernames = {}

def handle_client(client, username):
    while True:
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

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 7777)
    
    print("Iniciou o servidor de bate-papo")

    try:
        server.bind(server_address)
        server.listen()
    except Exception as e:
        return print(f'\nNão foi possível iniciar o servidor! Erro: {e}\n')

    while True:
        client, addr = server.accept()
        print(f'Cliente conectado com sucesso. IP: {addr}')
        
        # Solicita o nome de usuário do cliente
        client.send(' '.encode('utf-8'))
        username = client.recv(2048).decode('utf-8')
        
        clients.append(client)
        usernames[client] = username
        
        print(f'{username} está conectado conectado.')

        # Informa a todos os clientes sobre a nova conexão
        broadcast(f'{username} entrou no chat.'.encode('utf-8'), 'Servidor')

        thread = threading.Thread(target=handle_client, args=(client, username))
        thread.start()

if __name__ == "__main__":
    main()
