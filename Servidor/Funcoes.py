import hashlib
import struct
import Constantes as const

# Define a estrutura do pacote UDP
PACKET_FORMAT = "Iqf"
PACKET_SIZE = struct.calcsize(PACKET_FORMAT)

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


# Fecha a fatura
def fecha_fatura(usuario, consumo, mes):
    print("Entrou no fechamento de fatura")
    valor_fatura = consumo * const.TARIFA_ENERGIA
    usuario.fatura[mes] = (consumo, valor_fatura)

    if consumo >= media_faturas() + const.ALERTA_EXCESSIVO:
        usuario.alerta_consumo_excessivo == True
    else:
        usuario.alerta_consumo_excessivo == False

# Calcula média de todas as faturas
def media_faturas(usuario, fatura):
    media = 0.0
    for value in usuario.fatura.values():
        media += value

    return media

# Retorna o mês anterior
def mes_anterior(mes):
    if mes == "01":
        return "12"
    elif mes == "02":
        return "01"
    elif mes == "03":
        return "02"
    elif mes == "04":
        return "03"
    elif mes == "05":
        return "04"
    elif mes == "06":
        return "05"
    elif mes == "07":
        return "06"
    elif mes == "08":
        return "07"
    elif mes == "09":
        return "08"
    elif mes == "10":
        return "09"
    elif mes == "11":
        return "10"
    elif mes == "12":
        return "11"
