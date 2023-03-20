import json


class Usuario:
    def __init__(self, id, nome, endereco):
        self.id = id
        self.nome = nome
        self.endereco = endereco
        self.consumo = []
        self.fatura = {"1": 1.0, "2": 2.0, "3": 3.0}
        self.alerta_consumo_excessivo = False
        self.alerta_grande_variacao = False

    def toJson(self):
        x = {
            "id": self.id,
            "nome": self.nome,
            "endereco": self.endereco,
            "consumo_excessivo": self.alerta_consumo_excessivo,
            "grande_variacao": self.alerta_grande_variacao
        }
        x = json.dumps(x)
        return x

    def dataString(self):
        x = {
            "id": self.id,
            "nome": self.nome,
            "endereco": self.endereco,
            "consumo": self.consumo,
            "fatura": self.fatura,
        }
        return x
