import json
class FaturaEnergia:
    TARIFA_PADRAO = 0.6  # R$/kWh
    
    def __init__(self, nome_usuario, consumo, mes, ano, tarifa=TARIFA_PADRAO):
        self.nome_usuario = nome_usuario
        self.consumo = consumo
        self.mes = mes
        self.ano = ano
        self.tarifa = tarifa
        self.valorTotal = self.consumo * self.tarifa
    
    def calcular_total(self):
        return self.consumo * self.tarifa
    
    def toJson(self):
        x = {
            "usuario": self.nome_usuario,
            "consumo": self.consumo,
            "mes": self.mes,
            "ano": self.ano,
            "tarifa": self.tarifa,
            "valorTotal": self.total
        }
        x = json.dumps(x)
        return x
    
    def dataString(self):
        x = {
            "usuario": self.nome_usuario,
            "consumo": self.consumo,
            "mes": self.mes,
            "ano": self.ano,
            "tarifa": self.tarifa,
            "valorTotal": self.total
        }
        return x