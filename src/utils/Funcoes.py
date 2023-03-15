# Desempacota os dados
# Define a estrutura do pacote UDP
import hashlib
import struct

PACKET_FORMAT = "Iqf"
PACKET_SIZE = struct.calcsize(PACKET_FORMAT)


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
