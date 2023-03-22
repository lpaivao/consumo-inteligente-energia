import datetime
import random
import socket
import time
import threading

import Constantes as const
import Funcoes as fct


class SocketThread(threading.Thread):
    def __init__(self, sock, stop_event, client_id):
        super().__init__()
        self.acumulador = 0
        self.sock = sock
        self.stop_event = stop_event
        self.client_id = client_id
        self.consumo_adicional = 0.0

    def run(self):
        print(f"Servidor UDP iniciado na porta {const.UDP_PORT}...")
        while not self.stop_event.is_set():
            try:
                # Código para preparar os dados a serem enviados
                # Data e Horário
                timestamp = int(time.time())
                # Randomizador de consumo
                consumo = random.randint(1, 5)
                consumo = consumo + self.consumo_adicional
                # Criando um objeto datetime a partir do timestamp
                dt = datetime.datetime.fromtimestamp(timestamp)
                # Obtendo a data e o horário separadamente
                date = dt.strftime("%Y-%m-%d")  # formato YYYY-MM-DD
                hora = dt.strftime("%H:%M:%S")  # formato HH:MM:SS

                if fct.verifica_fechamento_fatura(date, hora):
                    self.acumulador = 0
                    time.sleep(54)
                else:
                    self.acumulador = self.acumulador + consumo
                    # Empacota os dados
                    packet = fct.create_packet(self.client_id, timestamp, self.acumulador)
                    # Faz o parse do desempacotamento apenas para fins da amostragem
                    parsed_data = fct.parse_packet(packet)
                    print(parsed_data)
                    # Envia o pacote
                    self.sock.sendto(packet, (const.HOST, const.UDP_PORT))
                    # Espera 5 segundos
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
            try:
                opcao = int(
                    input("Digite a opcao:\n[1] - Zerar consumo (Não aumenta nem diminui)\n[2] - Aumentar consumo ("
                          "Aumenta +5)\n[3] - "
                          "Diminuir consumo(Diminui -5)\n"))
                if opcao == 1:
                    socket_thread.consumo_adicional = 0.0
                elif opcao == 2:
                    socket_thread.consumo_adicional = socket_thread.consumo_adicional + 5.0
                elif opcao == 3:
                    socket_thread.consumo_adicional = socket_thread.consumo_adicional - 5.0
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        stop_event.set()
        socket_thread.join()


if __name__ == "__main__":
    main()
