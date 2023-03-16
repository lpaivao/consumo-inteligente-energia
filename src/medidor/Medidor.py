import datetime
import random
import socket
import time
import struct
import hashlib
import time
import threading

from src.utils import Constantes as const
import src.utils.Funcoes as fct

consumo_padrao_mensal = 150  # KwH
consumo_maior_mensal = 310
consumo_menor_mensal = 95

consumo_padrao_segundos = 0.05
consumo_maior_segundos = 0.1
consumo_menor_segundos = 0.03

consumo_inicial = consumo_padrao_segundos

# Define a estrutura do pacote UDP
PACKET_FORMAT = "Iqf"
PACKET_SIZE = struct.calcsize(PACKET_FORMAT)

# Empacota os dados


def create_packet(client_id, timestamp, energy):
    # Codifica os campos em bytes e empacota em um pacote UDP
    packed_data = struct.pack(PACKET_FORMAT, client_id, timestamp, energy)
    # Calcula um checksum/hash dos dados para garantir a integridade do pacote
    packet_hash = hashlib.md5(packed_data).digest()
    # Retorna o pacote UDP concatenando os dados e o hash
    return packed_data + packet_hash


# Desempacota os dados


def parse_packet(data):
    # Verifica se o pacote tem o tamanho correto e calcula o hash
    if len(data) != PACKET_SIZE + 16:
        raise ValueError("Invalid packet size")
    packet_data = data[:-16]
    packet_hash = data[-16:]
    # Verifica se o hash é válido
    if hashlib.md5(packet_data).digest() != packet_hash:
        raise ValueError("Invalid packet hash")
    # Desempacota os campos do pacote
    client_id, timestamp, energy = struct.unpack(PACKET_FORMAT, packet_data)
    # Retorna os dados desempacotados
    return client_id, timestamp, energy


class SocketThread(threading.Thread):
    def __init__(self, sock, stop_event, client_id):
        super().__init__()
        self.acumulador = 0
        self.sock = sock
        self.stop_event = stop_event
        self.client_id = client_id

    def run(self):
        print(f"Servidor UDP iniciado na porta {const.UDP_PORT}...")
        while not self.stop_event.is_set():
            try:
                # Código para preparar os dados a serem enviados
                # Data e Horário
                timestamp = int(time.time())
                # Randomizador de consumo
                # consumo = round(random.uniform(consumo_menor_segundos, consumo_maior_segundos), 3)
                consumo = random.randint(1, 5)
                # Criando um objeto datetime a partir do timestamp
                dt = datetime.datetime.fromtimestamp(timestamp)
                # Obtendo a data e o horário separadamente
                date = dt.strftime("%Y-%m-%d")  # formato YYYY-MM-DD
                hora = dt.strftime("%H:%M:%S")  # formato HH:MM:SS

                if fct.verifica_fechamento_fatura(date, time):
                    self.acumulador = 0
                    time.sleep(54)
                else:
                    self.acumulador = self.acumulador + consumo  # Empacota os dados
                    packet = create_packet(self.client_id, timestamp, self.acumulador)
                    # Faz o parse do desempacotamento
                    parsed_data = parse_packet(packet)
                    print(parsed_data)
                    # assert parsed_data == (self.client_id, timestamp, consumo)
                    self.sock.sendto(packet, (const.HOST, const.UDP_PORT))
                    time.sleep(5)

            except KeyboardInterrupt:
                self.stop_event.set()
                self.sock.close()


def main():
    client_id = int(
        input("Digite o ID do cliente que será associado ao medidor:\n"))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    stop_event = threading.Event()
    socket_thread = SocketThread(sock, stop_event, client_id)
    socket_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        stop_event.set()
        socket_thread.join()


if __name__ == "__main__":
    main()
