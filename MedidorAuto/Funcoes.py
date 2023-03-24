import hashlib
import struct
import Constantes as const

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


# Verifica se é o dia do fechamento da fatura
def verifica_fechamento_fatura(date, time):
    # Pega o dia e o mes separados
    date_format = date.split("-")
    dia = date_format[2]
    mes = date_format[1]
    # Pega a hora e o minuto separados
    time_format = time.split(":")
    hora = time_format[0]
    minuto = time_format[1]

    if dia == const.DIA_FECHAMENTO:
        if hora == "02":
            if minuto == "00":
                return True

    return False
