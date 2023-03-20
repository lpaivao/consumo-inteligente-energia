# Desempacota os dados
# Define a estrutura do pacote UDP
import hashlib
import struct
import Constantes as const

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


def fecha_fatura(usuario, consumo, mes):
    print("Entrou no fechamento de fatura")
    valor_fatura = consumo * const.TARIFA_ENERGIA
    usuario.fatura[mes] = {"consumo": consumo, "valor": valor_fatura}
    if (consumo >= media_faturas() + const.ALERTA_VARIACAO):
        usuario.alerta_grande_variacao == True
        if (consumo >= media_faturas() + const.ALERTA_EXCESSIVO):
            usuario.alerta_grande_variacao == True
        else:
            usuario.alerta_grande_variacao == False
    else:
        usuario.alerta_grande_variacao == False


def media_faturas(usuario, fatura):
    media = 0.0
    for value in usuario.fatura.values():
        media += value

    return media
