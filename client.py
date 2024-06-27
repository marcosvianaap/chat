import threading
import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 7777)

    try:
        client.connect(server_address)
    except Exception as e:
        return print(f'\nNão foi possível se conectar ao servidor! Erro: {e}\n')

    username = input('Usuário> ')
    client.send(username.encode('utf-8'))
    print('\nConectado')

    thread1 = threading.Thread(target=receive_messages, args=(client,))
    thread2 = threading.Thread(target=send_messages, args=(client, username))

    thread1.start()
    thread2.start()

def receive_messages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            if not msg:
                break
            print(msg + '\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break

def send_messages(client, username):
    while True:
        try:
            msg = input('\n')
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except:
            client.close()
            break

if __name__ == "__main__":
    main()
