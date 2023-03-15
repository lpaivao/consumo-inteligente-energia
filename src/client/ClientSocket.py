import socket
import select
import Constantes as const

CONTENT_TYPE = "application/json"

def run_socket_client_get(id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((const.HOST, const.TCP_PORT))
        print('Conectado ao servidor')
        # Envia uma mensagem para o servidor
        str = 'GET /usuario/?id={} HTTP/1.1\r\n\r\n'.format(id)
        s.sendall(str.encode("utf-8"))
        # Recebe a mensagem de volta do servidor
        data = s.recv(1024)
        print(f'Mensagem recebida do servidor: {data.decode()}')
        
def run_socket_client_get_fatura(id, mes):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((const.HOST, const.TCP_PORT))
        print('Conectado ao servidor')
        # Envia uma mensagem para o servidor
        str = 'GET /usuario/fatura/?id={}&mes={} HTTP/1.1\r\n\r\n'.format(id, mes)
        s.sendall(str.encode("utf-8"))
        # Recebe a mensagem de volta do servidor
        data = s.recv(1024)
        print(f'Mensagem recebida do servidor: {data.decode()}')
        
def run_socket_client_get_consumo(id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((const.HOST, const.TCP_PORT))
        print('Conectado ao servidor')
        # Envia uma mensagem para o servidor
        str = 'GET /usuario/consumo/?id={} HTTP/1.1\r\n\r\n'.format(id)
        s.sendall(str.encode("utf-8"))
        # Recebe a mensagem de volta do servidor
        data = s.recv(1024)
        print(f'Mensagem recebida do servidor: {data.decode()}')    
            
def run_socket_client_post():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((const.HOST, const.TCP_PORT))
        print('Conectado ao servidor')
        # Envia uma mensagem para o servidor
        str = 'POST /usuario/ HTTP/1.1\r\n\r\n{"id": 1, "nome": "lucas", "endereco": "rua a"}'
        s.sendall(str.encode("utf-8"))
        # Recebe a mensagem de volta do servidor
        data = s.recv(1024)
        print(f'Mensagem recebida do servidor: {data.decode()}')
        
def run_socket_client_delete(num):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((const.HOST, const.TCP_PORT))
        print('Conectado ao servidor')
        # Envia uma mensagem para o servidor
        str = 'DELETE /usuario/?id={} HTTP/1.1\r\n\r\n'.format(num)
        s.sendall(str.encode("utf-8"))
        # Recebe a mensagem de volta do servidor
        data = s.recv(1024)
        print(f'Mensagem recebida do servidor: {data.decode()}')
        
if __name__ == '__main__':
    try:
        while True:
            opt = int(input("Digite a opção:\n[1] - Fazer POST de um cliente pronto\n[2] - Fazer o GET de um cliente pelo ID\n[3] -  Fazer o DELETE de um cliente pelo ID\n"))
            if(opt == 1):
                run_socket_client_post()
            elif(opt == 2):
                opt2 = int(input("Digite a opção:\n[1] - Get de cliente 1\n[2] - Get de fatura 1\n[3] -  Get de consumo 1\n"))
                if(opt2 == 1):
                    run_socket_client_get(1)
                elif(opt2 == 2):
                    run_socket_client_get_fatura(1, 2)
                elif(opt2 == 3):
                    run_socket_client_get_consumo(1)
            elif(opt == 3):
                run_socket_client_delete(1)
            else:
                print("Opção Inválida, Tente novamente")
    except KeyboardInterrupt:
        pass