import urllib.parse
import json
from HttpUtils import *
import Usuario as user


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
        request_path, conn, lista_usuarios
):
    if "/usuario/?" in request_path:
        parametros_de_consulta = urllib.parse.parse_qs(
            urllib.parse.urlparse(request_path).query
        )
        try:
            # Obtendo o valor do Query Param 'id'
            id = int(parametros_de_consulta["id"][0])
            if id not in lista_usuarios.keys():
                body_response = {"Mensagem": "Id nao encontrado"}
                body_response = json.dumps(body_response)
                conn.sendall(NotFound(body_response))
                ##########################################
            else:
                # dados = lista_usuarios[id].__dict__
                # body = json.dumps(dados)
                body = lista_usuarios[id].toJson()
                response = OK(body)
                conn.sendall(response)
        except:
            response = BadRequest({"mensagem": "erro"})
            conn.sendall(response)

    elif request_path == "/usuario/":
        try:
            if len(lista_usuarios) == 0:
                body_response = {"Mensagem": "Nao tem usuarios cadastrados"}
                body_response = json.dumps(body_response)
                conn.sendall(NotFound(body_response))
            else:
                lista_all = []
                for usuario in lista_usuarios.values():
                    lista_all.append(usuario.toJson())

                body = {"Usuarios": lista_all}
                response = OK(body)
                conn.sendall(response)
        except:
            response = BadRequest({"mensagem": "erro"})
            conn.sendall(response)

    elif "/usuario/fatura/" in request_path:
        # Analisando a URL da solicitação para obter os parâmetros de consulta
        parametros_de_consulta = urllib.parse.parse_qs(
            urllib.parse.urlparse(request_path).query
        )
        try:
            # Obtendo o valor do Query Param 'id'
            id = int(parametros_de_consulta["id"][0])
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
        except:
            response = BadRequest({"mensagem": "erro"})
            conn.sendall(response)

    elif "/usuario/consumo/?" in request_path:
        # Analisando a URL da solicitação para obter os parâmetros de consulta
        parametros_de_consulta = urllib.parse.parse_qs(
            urllib.parse.urlparse(request_path).query
        )
        try:
            # Obtendo o valor do Query Param 'id'
            id = int(parametros_de_consulta["id"][0])

            if id not in lista_usuarios.keys():
                body_response = {"Mensagem": "Id nao encontrado"}
                body_response = json.dumps(body_response)
                conn.sendall(NotFound(body_response))
            else:
                print("consultar consumo de usuario de id: " + str(id))
                usuario = lista_usuarios[id]
                consumo = usuario.consumo

                response = OK({"consumo": consumo})

                conn.sendall(response)
        except:
            response = BadRequest({"mensagem": "erro"})
            conn.sendall(response)

    elif "/usuario/consumo/data/?" in request_path:
        # Analisando a URL da solicitação para obter os parâmetros de consulta
        parametros_de_consulta = urllib.parse.parse_qs(
            urllib.parse.urlparse(request_path).query
        )
        try:
            # Obtendo o valor do Query Param 'id'
            id = int(parametros_de_consulta["id"][0])
            data = parametros_de_consulta["data"][0]

            if id not in lista_usuarios.keys():
                body_response = {"Mensagem": "Id nao encontrado"}
                body_response = json.dumps(body_response)
                conn.sendall(NotFound(body_response))
                ##########################################
            else:
                print("consultar consumo por data de usuario de id: " + str(id))
                usuario = lista_usuarios[id]
                consumo = usuario.consumo

                lista_temporaria = []
                for tupla in consumo:
                    print(tupla[0])
                    if tupla[0] == data:
                        lista_temporaria.append(tupla)

                if len(lista_temporaria) != 0:
                    response = OK({"dia": data, "consumo": lista_temporaria})
                else:
                    response = NotFound({"consumo": "Nao tem consumos com essa data"})

                conn.sendall(response)
        except:
            response = BadRequest({"mensagem": "erro"})
            conn.sendall(response)

    elif "/usuario/consumo/horario/?" in request_path:
        # Analisando a URL da solicitação para obter os parâmetros de consulta
        parametros_de_consulta = urllib.parse.parse_qs(
            urllib.parse.urlparse(request_path).query
        )
        try:
            # Obtendo o valor do Query Param 'id'
            id = int(parametros_de_consulta["id"][0])
            data = parametros_de_consulta["data"][0]
            horario = parametros_de_consulta["horario"][0]

            if id not in lista_usuarios.keys():
                body_response = {"Mensagem": "Id nao encontrado"}
                body_response = json.dumps(body_response)
                conn.sendall(NotFound(body_response))
                ##########################################
            else:
                print("consultar consumo por horario de usuario de id: " + str(id))
                usuario = lista_usuarios[id]
                consumo = usuario.consumo

                lista_temporaria_data = []
                for tupla in consumo:
                    if tupla[0] == data:
                        lista_temporaria_data.append(tupla)

                if len(lista_temporaria_data) != 0:
                    lista_temporaria_horario = []
                    for tupla in lista_temporaria_data:
                        if horario in tupla[1]:
                            lista_temporaria_horario.append(tupla)
                    response = OK({"dia": data, "horario": horario, "consumo": lista_temporaria_horario})
                else:
                    response = NotFound({"consumo": "Nao tem consumos com esse horario"})

                conn.sendall(response)
        except:
            response = BadRequest({"mensagem": "erro"})
            conn.sendall(response)

    elif "/usuario/alerta/variacao/?" in request_path:
        # Analisando a URL da solicitação para obter os parâmetros de consulta
        parametros_de_consulta = urllib.parse.parse_qs(
            urllib.parse.urlparse(request_path).query
        )
        try:
            # Obtendo o valor do Query Param 'id'
            id = int(parametros_de_consulta["id"][0])

            if id not in lista_usuarios.keys():
                body_response = {"Mensagem": "Id nao encontrado"}
                body_response = json.dumps(body_response)
                conn.sendall(NotFound(body_response))
                ##########################################
            else:
                print("consultar alerta de usuario de id: " + str(id))
                usuario = lista_usuarios[id]

                if usuario.alerta_grande_variacao == True:
                    response = OK({"Alerta!!": "Sua Ultima fatura possui grande variacao"})
                else:
                    response = OK({"Sem alertas": "Sua Ultima fatura está na media"})

                conn.sendall(response)
        except:
            response = BadRequest({"mensagem": "erro"})
            conn.sendall(response)

    elif "/usuario/alerta/excesso/?" in request_path:
        # Analisando a URL da solicitação para obter os parâmetros de consulta
        parametros_de_consulta = urllib.parse.parse_qs(
            urllib.parse.urlparse(request_path).query
        )
        try:
            # Obtendo o valor do Query Param 'id'
            id = int(parametros_de_consulta["id"][0])
            print("consultar alerta de usuario de id: " + str(id))
            usuario = lista_usuarios[id]

            if id not in lista_usuarios.keys():
                body_response = {"Mensagem": "Id nao encontrado"}
                body_response = json.dumps(body_response)
                conn.sendall(NotFound(body_response))
                ##########################################
            else:
                if (usuario.alerta_consumo_excessivo == True):
                    response = OK({"Alerta!!": "Sua Ultima fatura possui um consumo excessivo"})
                else:
                    response = OK({"Sem alertas": "Sua Ultima fatura está na media de consumo das outras"})

                conn.sendall(response)
        except:
            response = BadRequest({"mensagem": "erro"})
            conn.sendall(response)


def receivePost(
        request_path,
        body,
        conn,
        lista_usuarios,
):
    if request_path == "/usuario/cadastro/":
        try:
            data = json.loads(body)
            # Faça algo com os dados recebidos
            id = data["id"]
            nome = data["nome"]
            endereco = data["endereco"]

            if id in lista_usuarios.keys():
                body_response = {"Mensagem": "Usuario ja cadastrado"}
                body_response = json.dumps(body_response)
                conn.sendall(NotFound(body_response))
            else:
                usuario = user.Usuario(id, nome, endereco)
                lista_usuarios[id] = usuario
                body_response = {"mensagem": "Cadastro feito com sucesso!", "id": id, "nome": nome, "endereco": endereco}
                # body_response = {"id": id, "nome": nome, "endereco": endereco}
                body_response = json.dumps(body_response)

                conn.sendall(OK(body_response))
        except:
            response = BadRequest({"mensagem": "erro"})
            conn.sendall(response)


def receiveDelete(
        request_path, conn, lista_usuarios
):
    if "/usuario/delete/?" in request_path:
        parametros_de_consulta = urllib.parse.parse_qs(
            urllib.parse.urlparse(request_path).query
        )
        try:
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
        except:
            response = BadRequest({"mensagem": "erro"})
            conn.sendall(response)


# Protocolos de resposta sem body
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
