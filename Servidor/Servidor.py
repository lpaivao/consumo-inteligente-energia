import datetime
import time
import socket
import threading
import Constantes as const
import Funcoes as fct
import Usuario as user
from HttpUtils import *

# Variaveis
lista = {}


def handle_client(cliente, addr, evento):
    with cliente:
        while not evento.is_set():
            print(f"Conexão estabelecida por {addr}")
            data = cliente.recv(4096)  # recebe os dados enviados pelo cliente
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

        cliente.close()


def tcp_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.setblocking(False)
        s.bind((const.HOST, const.TCP_PORT))
        s.listen(3)  # coloca o socket em modo de escuta
        print(f"Servidor iniciado em {const.HOST}:{const.TCP_PORT}")

        while True:
            try:
                cliente, addr = s.accept()  # aguarda a conexão de um cliente
                # cliente.setblocking(False)
                print(f"Cliente conectado: {addr}")
                # cria uma nova thread para lidar com o cliente
                evento = threading.Event()
                thread = threading.Thread(
                    target=handle_client, args=(cliente, addr, evento))
                thread.start()
                evento.set()
                thread.join()
            except KeyboardInterrupt:
                s.close()
                break


def udp_listener():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((const.HOST, const.UDP_PORT))

    while True:
        try:
            # Recebe a mensagem
            data, addr = udp_sock.recvfrom(4096)
            # Desempacota os dados
            parsed_data = fct.parse_packet(data)
            # Separa os dados desempacotados
            client_id = parsed_data[0]
            timestamp = parsed_data[1]
            consumo = parsed_data[2]
            consumo = round(consumo / 10000, 4)
            print(consumo)

            if client_id in lista.keys():
                # Criando um objeto datetime a partir do timestamp
                dt = datetime.datetime.fromtimestamp(timestamp)
                # Obtendo a data e o horário separadamente
                date = dt.strftime("%Y-%m-%d")  # formato YYYY-MM-DD
                hora = dt.strftime("%H:%M:%S")  # formato HH:MM:SS

                # Pega o mes
                date_format = date.split("-")
                mes = date_format[1]
                # Faz a tupla para adicionar a lista de consumo do cliente
                tupla_consumo = (date, hora, consumo)
                usuario = lista[client_id]
                usuario.consumo.append(tupla_consumo)

                # Verifica se houve uma grande variação no consumo em relação a fatura do mês anterior
                if fct.mes_anterior(mes) in usuario.fatura.keys():
                    if consumo >= usuario.fatura[fct.mes_anterior(mes)][0] + const.ALERTA_VARIACAO:
                        usuario.alerta_grande_variacao = True

                # Verifica se está no dia e horário para fechamento da fatura
                if fct.verifica_fechamento_fatura(date, hora):
                    fct.fecha_fatura(usuario, consumo, mes)

        except KeyboardInterrupt:
            udp_sock.close()
            break


if __name__ == "__main__":

    udp_thread = threading.Thread(target=udp_listener)
    udp_thread.start()

    usuario1 = user.Usuario(1, "lucas", "rua a")
    usuario2 = user.Usuario(2, "gabriela", "rua b")

    lista[1] = usuario1
    lista[2] = usuario2

    tcp_listener()

    while True:
        try:
            pass
        except KeyboardInterrupt:
            udp_thread.join()
            break
