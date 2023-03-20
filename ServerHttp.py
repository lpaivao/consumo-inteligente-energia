import json
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from HttpUtils import *

from Usuario import Usuario

HOST = "127.0.0.1"  # Endereço IP do servidor
PORT = 8000  # Porta a ser usada

lista = {}
lista_all = {}


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            message = "Hello, World!"
            self.wfile.write(message.encode())

        elif self.path == "/usuario":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            dados = lista_all
            print(lista_all)
            # dados = list(lista.keys())
            response = json.dumps(dados)
            self.wfile.write(response.encode(encoding="utf-8"))

        elif "/usuario?" in self.path:
            str_aux = self.path.split("?")
            str = str_aux[1]
            indice_aux = str.split("=")
            indice = int(indice_aux[0])
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            dados = lista[indice].__dict__
            response = json.dumps(dados)
            self.wfile.write(response.encode(encoding="utf-8"))

        if self.path == "/usuario/fatura/":
            # Analisando a URL da solicitação para obter os parâmetros de consulta
            parametros_de_consulta = urllib.parse.parse_qs(
                urllib.parse.urlparse(self.path).query
            )
            # Obtendo o valor do Query Param 'id'
            id = parametros_de_consulta.get("id", None)

            print("consultar fatura de usuario de id: " + id[0])

            usuario = lista[id[0]]
            fatura = usuario.fatura
            response = json.dumps(fatura)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response.encode(encoding="utf-8"))

        if self.path == "/usuario/consumo/":
            # Analisando a URL da solicitação para obter os parâmetros de consulta
            parametros_de_consulta = urllib.parse.parse_qs(
                urllib.parse.urlparse(self.path).query
            )
            # Obtendo o valor do Query Param 'id'
            id = parametros_de_consulta.get("id", None)
            print("consultar consumo de usuario de id: " + id[0])
            usuario = lista[id]
            consumo = int(usuario.consumo)

            if consumo:
                str_json = {"consumo": consumo}
                response = json.dumps(str_json)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.encode(encoding="utf-8"))

    def do_POST(self):
        if self.path == "/usuario":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))
            print(self.requestline)

            # Faça algo com os dados recebidos
            id = data["id"]
            nome = data["nome"]
            endereco = data["endereco"]
            usuario = Usuario(id, nome, endereco)
            lista[id] = usuario
            lista_all[id] = usuario.dataString()
            # ...

            response_data = {"mensagem": "Requisicao POST recebida com sucesso!"}
            response = json.dumps(response_data)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response.encode())

    def do_PUT(self):
        content_length = int(self.headers["Content-Length"])
        put_data = self.rfile.read(content_length)
        data = json.loads(put_data.decode("utf-8"))
        # Faça algo com os dados recebidos

        # ...
        response_data = {"mensagem": "Requisicao PUT recebida com sucesso!"}
        response = json.dumps(response_data)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode())

    def do_DELETE(self):
        # str_aux = self.path.split("/")
        # str = int(str_aux[2])
        # parsed_path = urllib.parse.urlparse(self.path)
        # query_params = urllib.parse.parse_qs(parsed_path.query)
        # id = query_params['id'][0]
        # Faça algo com o ID recebido

        # Analisando a URL da solicitação para obter os parâmetros de consulta
        parametros_de_consulta = urllib.parse.parse_qs(
            urllib.parse.urlparse(self.path).query
        )

        # Obtendo o valor do Query Param 'id'
        id = parametros_de_consulta.get("id", None)
        print("id a remover = " + id[0])
        if id is not None:
            # Realizando a ação de delete com o ID obtido
            # ...
            removido = lista.pop(int(id[0]))
            lista_all.pop(int(id[0]))
            # ...
            response_data = removido.dataString()
            response = json.dumps(response_data)
            self.send_response(200)  # OK #resposta sem conteúdo
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_error(400, "O parâmetro 'id' é obrigatório.")


def run_http_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Servidor http iniciado na porta {}\n".format(PORT))
    httpd.serve_forever()


if __name__ == "__main__":
    run_http_server()
