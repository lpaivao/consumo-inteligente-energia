import socket

UDP_PORT = 18000
TCP_PORT = 15000
HOST = socket.gethostbyname(socket.gethostname())
TIMEOUT = 10

TARIFA_ENERGIA = 0.65  # tarifa da bahia B1-residencial
DIA_FECHAMENTO = "10"

ALERTA_EXCESSIVO = 150.0
ALERTA_VARIACAO = 100.0

consumo_padrao_mensal = 150  # KwH
consumo_maior_mensal = 310
consumo_menor_mensal = 95

consumo_padrao_segundos = 0.0005
consumo_maior_segundos = 0.001
consumo_menor_segundos = 0.0003
