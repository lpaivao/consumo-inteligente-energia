import datetime
import select

import schedule

import socket
import threading
import time
import socket
import threading

import src.utils.Constantes as const
import src.utils.Funcoes as fct
import src.entities.Usuario as user

# from ServerHttp import RequestHandler as rh
from src.entities.Usuario import Usuario
from src.utils.HttpUtils import *

# Constantes


# Variaveis
lista = {}
threads = []


class ServidorTCP:
    def __init__(self, ip, porta, tempo_maximo):
        self.ip = ip
        self.porta = porta
        self.tempo_maximo = tempo_maximo
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.setblocking(False)
        self.servidor.bind((ip, porta))
        self.threads = []
        self.rodando = False

    def inicia(self):
        self.servidor.listen()
        self.rodando = True
        print(f"Servidor TCP iniciado em {self.ip}:{self.porta}")

        # inicia a thread que exibe as threads em execução
        thread_mostra_threads = threading.Thread(target=self.mostra_threads)
        thread_mostra_threads.start()

        # registra o socket do servidor na lista de leitura
        inputs = [self.servidor]

        try:
            while self.rodando:
                # espera por entradas de leitura e escrita
                leitura, escrita, excecao = select.select(inputs, [], [], self.tempo_maximo)

                # percorre as entradas de leitura
                for s in leitura:
                    # se for o socket do servidor, aceita uma conexão
                    if s is self.servidor:
                        cliente, endereco = self.servidor.accept()
                        if len(endereco) < 2:
                            print("Endereço inválido")
                            continue
                        porta = endereco[1]
                        print(f"Conexão estabelecida com {endereco[0]}:{endereco[1]}")
                        thread = threading.Thread(
                            target=self.escuta_cliente, args=(cliente, endereco))
                        thread.start()
                        self.threads.append((cliente, thread))
                # percorre as exceções
                for s in excecao:
                    print(f"Erro na conexão com {s.getpeername()}")

        except KeyboardInterrupt:
            self.encerra()

    def escuta_cliente(self, cliente, addr):
        try:
            while True:
                mensagem = cliente.recv(1024)
                if not mensagem:
                    break

                http_request = mensagem.decode()
                print(http_request)
                (
                    request_method,
                    request_path,
                    request_protocol,
                    headers,
                    body_part,
                ) = splitHttpReq(http_request)

                if request_method == "GET":
                    print("entrou no get")
                    receiveGet(
                        request_method,
                        request_path,
                        request_protocol,
                        headers,
                        cliente,
                        addr,
                        lista,
                    )

                elif request_method == "POST":
                    receivePost(
                        request_method,
                        request_path,
                        request_protocol,
                        headers,
                        body_part,
                        cliente,
                        addr,
                        lista,
                    )

                elif request_method == "DELETE":
                    receiveDelete(
                        request_method,
                        request_path,
                        request_protocol,
                        headers,
                        cliente,
                        addr,
                        lista,
                    )

        except BlockingIOError:
            pass
        except ConnectionResetError:
            print(f"Conexão resetada pelo cliente {addr}")
        except Exception as e:
            print(f"Erro na conexão com {cliente.getpeername()}: {e}")
        finally:
            print(f"Conexão encerrada com {cliente.getpeername()}")
            cliente.close()
            for i, (c, t) in enumerate(self.threads):
                if c == cliente:
                    try:
                        self.threads.pop(i)
                    except IndexError:
                        pass
                    try:
                        t.join()
                    except Exception as e:
                        print(f"Erro ao encerrar thread: {e}")

    def mostra_threads(self):
        while self.rodando:
            try:
                print("Threads em execução:")
                for c, t in self.threads:
                    print(
                        f"Thread {t.ident}: atendendo cliente {c.getpeername()}")
                time.sleep(5)
            except OSError:
                print("Cliente desconectado")

    def encerra(self):
        self.rodando = False
        for c, t in self.threads:
            t.join()
            c.close()
        self.servidor.close()
        print("Servidor TCP finalizado")


def udp_listener():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((const.HOST, const.UDP_PORT))

    try:
        while True:
            data, addr = udp_sock.recvfrom(1024)
            print(f"Received message from {addr}: {data}")
            # Process data and send to client through TCP socket
            #
            parsed_data = fct.parse_packet(data)
            client_id = parsed_data[0]
            timestamp = parsed_data[1]
            consumo = parsed_data[2]

            if client_id in lista.keys():
                # Criando um objeto datetime a partir do timestamp
                dt = datetime.datetime.fromtimestamp(timestamp)
                # Obtendo a data e o horário separadamente
                date = dt.strftime("%Y-%m-%d")  # formato YYYY-MM-DD
                time = dt.strftime("%H:%M:%S")  # formato HH:MM:SS

                # Pega o dia e o mes separados
                date_format = date.split("-")
                dia = date_format[2]
                mes = date_format[1]

                # Faz a tupla para adicionar a lista de consumo do cliente
                tupla_consumo = (date, time, consumo)
                usuario = lista[client_id]
                usuario.consumo.append(tupla_consumo)

                if dia == const.DIA_FECHAMENTO:
                    fecha_fatura(usuario, consumo, mes)

    except KeyboardInterrupt:
        pass


def fecha_fatura(usuario, consumo, mes):
    valor_fatura = consumo * const.TARIFA_ENERGIA
    usuario.fatura[mes] = {"consumo": consumo, "valor": valor_fatura}


def handle_client(cliente, addr, evento):
    with cliente:
        while not evento.is_set():
            print(f"Conexão estabelecida por {addr}")
            data = cliente.recv(1024)  # recebe os dados enviados pelo cliente
            if data:
                http_request = data.decode()

                (
                    request_method,
                    request_path,
                    request_protocol,
                    headers,
                    body_part,
                ) = splitHttpReq(http_request)

                if request_method == "GET":
                    receiveGet(
                        request_path,
                        cliente,
                        lista,
                    )

                elif request_method == "POST":
                    receivePost(
                        request_path,
                        body_part,
                        cliente,
                        lista,
                    )

                elif request_method == "DELETE":
                    receiveDelete(
                        request_path,
                        cliente,
                        lista,
                    )

                # print("\n\n")
                # print(repr(http_request))
                # print(f"Mensagem recebida de {addr}: {http_request}")


def tcp_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((const.HOST, const.TCP_PORT))
        s.listen()  # coloca o socket em modo de escuta
        print(f"Servidor iniciado na porta {const.TCP_PORT}...")

        while True:
            cliente, addr = s.accept()  # aguarda a conexão de um cliente
            print(f"Cliente conectado: {addr}")
            # cria uma nova thread para lidar com o cliente
            evento = threading.Event()
            thread = threading.Thread(
                target=handle_client, args=(cliente, addr, evento))
            thread.start()

            evento.set()
            thread.join()


if __name__ == "__main__":
    udp_thread = threading.Thread(target=udp_listener)
    udp_thread.start()

    usuario1 = user.Usuario(1, "lucas", "rua a")
    usuario2 = user.Usuario(2, "gabriela", "rua b")

    lista[1] = usuario1
    lista[2] = usuario2

    #servidor = ServidorTCP(const.HOST, const.TCP_PORT, 5)
    #servidor.inicia()

    tcp_thread = threading.Thread(target=tcp_listener)
    tcp_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
