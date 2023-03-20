import json
import random
import Constantes as const

class Usuario:
    def __init__(self, id, nome, endereco):
        self.id = id
        self.nome = nome
        self.endereco = endereco
        self.consumo = []
        consumo_fatura1 = random.randint(const.consumo_menor_mensal, const.consumo_maior_mensal)
        consumo_fatura2 = random.randint(const.consumo_padrao_mensal, const.consumo_maior_mensal)
        consumo_fatura3 = random.randint(const.consumo_padrao_mensal, const.consumo_maior_mensal+250)
        self.fatura = {"01": (consumo_fatura1, consumo_fatura1*const.TARIFA_ENERGIA),
                       "02": (consumo_fatura2, consumo_fatura2*const.TARIFA_ENERGIA),
                       "03": (consumo_fatura3, consumo_fatura3*const.TARIFA_ENERGIA)}
        self.alerta_consumo_excessivo = False
        self.alerta_grande_variacao = False
        media = (self.fatura["01"][0] + self.fatura["02"][0])/2
        if self.fatura["03"][0] >= media + const.ALERTA_EXCESSIVO:
            self.alerta_consumo_excessivo = True

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
