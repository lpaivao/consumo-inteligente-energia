# ------------------------------------- HTTP Request example -------------------------------------
# GET /hello.txt HTTP/1.1
# User-Agent     : curl/7.64.1
# Host           : www.example.com
# Accept-Language: en, mi

##------------------------------------- HTTP Response example -------------------------------------
# HTTP/1.1 200 OK
# Date          : Mon, 27 Jul 2009 12: 28: 53 GMT
# Server        : Apache
# Last-Modified : Wed, 22 Jul 2009 19: 15: 56 GMT
# ETag          : "34aa387-d-1568eb00"
# Accept-Ranges : bytes
# Content-Length: 51
# Vary          : Accept-Encoding
# Content-Type  : text/plain
# Hello World! My content includes a trailing CRLF.
import json
import urllib.parse
import urllib.request

import socket
import select
import threading

from ServerHttp import RequestHandler as rh
from Usuario import Usuario
from utils.HttpUtils import *


def splitHttpReq(http_request):
    # exemplo de string de requisição HTTP
    # http_request = 'POST /api/data HTTP/1.1\r\nContent-Type: application/json\r\nContent-Length: 23\r\n\r\n{"key": "value", "key2": 2}'

    # dividir a string em três partes

    request_parts = http_request.split("\r\n\r\n")
    header_part = request_parts[0]
    body_part = request_parts[1]

    header_lines = header_part.split("\r\n")
    request_line = header_lines[0]
    headers = header_lines[1:]

    request_method, request_path, request_protocol = request_line.split(" ")

    # Exibindo as partes da requisição HTTP separadas
    # print(request_method)  # POST
    # print(request_path)    # /api/data
    # print(request_protocol) # HTTP/1.1
    # print(headers)         # ['Content-Type: application/json', 'Content-Length: 23']
    # print(body_part)       # {"key": "value", "key2": 2}

    return request_method, request_path, request_protocol, headers, body_part


def splitHttpResp(http_response):
    # exemplo de string de resposta HTTP
    # http_response = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 17\r\n\r\n{"status": "ok"}'

    # dividir a string em duas partes
    response_parts = http_response.split("\r\n\r\n")
    header_part = response_parts[0]
    body_part = response_parts[1]

    header_lines = header_part.split("\r\n")
    response_status = header_lines[0]
    headers = header_lines[1:]

    protocol, status_code, status_text = response_status.split(" ")

    # Exibindo as partes da resposta HTTP separadas
    # print(protocol)      # HTTP/1.1
    # print(status_code)   # 200
    # print(status_text)   # OK
    # print(headers)       # ['Content-Type: application/json', 'Content-Length: 17']
    # print(body_part)     # {"status": "ok"}

    return headers, body_part


def receiveGet(
    request_method, request_path, request_protocol, headers, conn, addr, lista_usuarios
):
    if "/usuario/?" in request_path:
        parametros_de_consulta = urllib.parse.parse_qs(
            urllib.parse.urlparse(request_path).query
        )

        # Obtendo o valor do Query Param 'id'
        id = int(parametros_de_consulta["id"][0])
        if id not in lista_usuarios.keys():
            body_response = {"Mensagem": "Id nao encontrado"}
            body_response = json.dumps(body_response)
            conn.sendall(NotFound(body_response))

        else:
            dados = lista_usuarios[id].__dict__
            body = json.dumps(dados)
            response = OK(body)

            conn.sendall(response)

    elif "/usuario/fatura/" in request_path:
        # Analisando a URL da solicitação para obter os parâmetros de consulta
        parametros_de_consulta = urllib.parse.parse_qs(
            urllib.parse.urlparse(request_path).query
        )
        # Obtendo o valor do Query Param 'id'
        id = parametros_de_consulta["id"][0]
        mes = parametros_de_consulta["mes"][0]
        if id not in lista_usuarios.keys():
            body_response = {"Mensagem": "Id nao encontrado"}
            body_response = json.dumps(body_response)
            conn.sendall(NotFound(body_response))
        else:
            usuario = lista_usuarios[int(id)]
            if mes not in usuario.fatura.keys():
                body_response = {"Mensagem": "Mes nao encontrado"}
                body_response = json.dumps(body_response)
                conn.sendall(NotFound(body_response))
            else:
                fatura = usuario.fatura[mes[0]]
                fatura = {"valor da fatura": fatura}
                body = json.dumps(fatura)

                response = OK(body)
                conn.sendall(response)

    elif "/usuario/consumo/?" in request_path:
        # Analisando a URL da solicitação para obter os parâmetros de consulta
        parametros_de_consulta = urllib.parse.parse_qs(
            urllib.parse.urlparse(request_path).query
        )
        # Obtendo o valor do Query Param 'id'
        id = parametros_de_consulta.get("id", None)
        print("consultar consumo de usuario de id: " + id[0])
        usuario = lista_usuarios[int(id[0])]
        consumo = usuario.consumo

        response = OK({"consumo": consumo})

        conn.sendall(response)


def receivePost(
    request_method,
    request_path,
    request_protocol,
    headers,
    body,
    conn,
    addr,
    lista_usuarios,
):
    if request_path == "/usuario/cadastro/":
        data = json.loads(body)

        # Faça algo com os dados recebidos
        id = data["id"]
        nome = data["nome"]
        endereco = data["endereco"]

        usuario = Usuario(id, nome, endereco)
        lista_usuarios[id] = usuario
        # ...

        # response_data = {"mensagem": "Cadastro feito com sucesso!", "id": id, "nome": nome, "endereco": endereco}
        body_response = {"id": id, "nome": nome, "endereco": endereco}
        body_response = json.dumps(body_response)

        conn.sendall(OK(body_response))


def receiveDelete(
    request_method, request_path, request_protocol, headers, conn, addr, lista_usuarios
):
    if "/usuario/delete/?" in request_path:
        print("entrou")
        parametros_de_consulta = urllib.parse.parse_qs(
            urllib.parse.urlparse(request_path).query
        )

        # Obtendo o valor do Query Param 'id'
        id = int(parametros_de_consulta["id"][0])
        if id not in lista_usuarios.keys():
            body_response = {"Mensagem": "Id nao encontrado"}
            body_response = json.dumps(body_response)
            conn.sendall(NotFound(body_response))
        else:
            # Realizando a ação de delete com o ID obtido
            # ...
            removido = lista_usuarios.pop(id)
            # ...
            response_data = removido.dataString()
            body_response = json.dumps(response_data)
            conn.sendall(OK(body_response))


# Protocolos de resposta sem body
def OK():
    return "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n".encode()


def BadRequest():
    return "HTTP/1.1 400 Bad Request\r\n\r\n".encode()


def NotFound():
    return "HTTP/1.1 404 Not Found\r\n\r\n".encode()


def InternalServerError():
    return "HTTP/1.1 500 Internal Server Error\r\n\r\n".encode()


def Created():
    return "HTTP/1.1 201 Created\r\n\r\n".encode()


# Protocolos de resposta com body em JSON
def OK(body):
    return "HTTP/1.1 200 OK\r\n\r\n{}".format(body).encode()


def BadRequest(body):
    return "HTTP/1.1 400 Bad Request\r\n\r\n{}".format(body).encode()


def NotFound(body):
    return "HTTP/1.1 404 Not Found\r\n\r\n{}".format(body).encode()


def InternalServerError(body):
    return "HTTP/1.1 500 Internal Server Error\r\n\r\n{}".format(body).encode()


def Created(body):
    return "HTTP/1.1 201 Created{}".format(body).encode()
