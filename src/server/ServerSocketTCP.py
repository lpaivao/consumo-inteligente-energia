import datetime

from sched import scheduler
import sched

# from schedule import Scheduler
import socket
import threading
import time
import socket
import threading

# import requests
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer

import utils.Constantes as const
import utils.Funcoes as fct


# from ServerHttp import RequestHandler as rh
from entities.Usuario import Usuario
from utils.HttpUtils import *

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

        try:
            while self.rodando:
                cliente, endereco = self.servidor.accept()
                print(f"Conexão estabelecida com {endereco[0]}:{endereco[1]}")
                thread = threading.Thread(
                    target=self.escuta_cliente, args=(cliente, endereco)
                )
                thread.start()
                self.threads.append((cliente, thread, time.time()))
        except KeyboardInterrupt:
            self.encerra()

    def escuta_cliente(self, conn, addr):
        agendador = sched.scheduler()
        agendador.every(self.tempo_maximo).seconds.do(self.interrupcao_thread, conn)
        while True:
            print(f"Conexão estabelecida por {addr}")
            data = conn.recv(1024)  # recebe os dados enviados pelo cliente
            if not data:
                break

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
                    request_method,
                    request_path,
                    request_protocol,
                    headers,
                    conn,
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
                    conn,
                    addr,
                    lista,
                )

            elif request_method == "DELETE":
                receiveDelete(
                    request_method,
                    request_path,
                    request_protocol,
                    headers,
                    conn,
                    addr,
                    lista,
                )

            agendador.cancel_jobs()
            agendador.every(self.tempo_maximo).seconds.do(self.interrupcao_thread, conn)

        print(f"Conexão encerrada com {conn.getpeername()}")
        conn.close()
        for c, t, _ in self.threads:
            if c == conn:
                t.join()
                self.threads.remove((c, t, _))

    def interrupcao_thread(self, cliente):
        print(
            f"Thread atendendo {cliente.getpeername()} interrompida após {self.tempo_maximo} segundos"
        )
        cliente.close()
        for c, t, _ in self.threads:
            if c == cliente:
                t.join()
                self.threads.remove((c, t, _))
                nova_thread = threading.Thread(target=self.escuta_cliente, args=(c,))
                nova_thread.start()
                self.threads.append((c, nova_thread, time.time()))

    def encerra(self):
        self.rodando = False
        for c, t, _ in self.threads:
            t.join()
            c.close()
        self.servidor.close()
        print("Servidor TCP finalizado")

    def mostra_threads(self):
        while self.rodando:
            print("Threads em execução:")
            for c, t in self.threads:
                print(f"Thread {t.ident}: atendendo cliente {c.getpeername()}")
            time.sleep(5)


def udp_listener():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((const.HOST, const.UDP_PORT))

    while True:
        data, addr = udp_sock.recvfrom(1024)
        print(f"Received message from {addr}: {data}")
        # Process data and send to client through TCP socket
        #
        parsed_data = fct.parse_packet(data)
        client_id = parsed_data[0]
        timestamp = parsed_data[1]
        consumo = parsed_data[2]

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


def fecha_fatura(usuario, consumo, mes):
    valor_fatura = consumo * const.TARIFA_ENERGIA
    usuario.fatura[mes] = {"consumo": consumo, "valor": valor_fatura}


def handle_client(conn, addr, evento):
    with conn:
        while not evento.is_set():
            print(f"Conexão estabelecida por {addr}")
            data = conn.recv(1024)  # recebe os dados enviados pelo cliente
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
                        request_method,
                        request_path,
                        request_protocol,
                        headers,
                        conn,
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
                        conn,
                        addr,
                        lista,
                    )

                elif request_method == "DELETE":
                    receiveDelete(
                        request_method,
                        request_path,
                        request_protocol,
                        headers,
                        conn,
                        addr,
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
            conn, addr = s.accept()  # aguarda a conexão de um cliente
            print(f"Cliente conectado: {addr}")
            # cria uma nova thread para lidar com o cliente
            evento = threading.Event()
            thread = threading.Thread(target=handle_client, args=(conn, addr, evento))
            thread.start()

            evento.set()
            thread.join()


if __name__ == "__main__":
    udp_thread = threading.Thread(target=udp_listener)
    udp_thread.start()

    servidor = ServidorTCP(const.HOST, const.TCP_PORT, 5)
    servidor.inicia()

    # tcp_thread = threading.Thread(target=tcp_listener)
    # tcp_thread.start()
