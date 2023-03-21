# Consumo de energia inteligente

## Contexto
Desenvolvimento de um protótipo em que os dados serão agregrados visando monitorar o consumo excessivo de energia, medir o consumo de cada cliente, gerar a fatura a ser paga, bem como alertar sobre um possível consumo excessivo de energia ou grande variação na conta de um usuário. Também, os usuários do serviço podem acessar o sistema de forma online para acompanhar o consumo de energia, com datas/horários específicos do consumo e o total acumulado.

## Produto
Os seguintes requisitos do problema foram atendidos:

- [x] Medir o consumo de cada cliente
- [x] Gerar a fatura a ser paga
- [x] Alertar sobre consumo excessivo
- [x] Alertar sobre grande variação
- [x] Acompanhar o consumo de energia com datas/horários específicos
- [x] Visualizar o total acumulado

O produto está dividido em dois módulos:
- Módulo do servidor
- Módulo do medidor

### Servidor

- Servidor.py: Arquivo principal onde estão os sockets para a comunicação entre cliente-servidor-medidor. Possui dois sockets principais: um socket TCP que escuta as requisições do cliente, e um socket UDP que escuta as informações enviadas do medidor.
- HttpUtils.py: Conjunto de funções utilitárias que tratam as requisições HTTP que serão recebidas pelo servidor principal. Possui, por exemplo, funções para receber requisições GET, POST e DELETE e enviar a resposta de volta para o cliente. Além disso, possui uma função que divide a requisição/resposta HTTP em vários pedaços diferentes e retorna essas partes.
- Funcoes.py: Possui algumas funções mais genéricas com objetivos como: desempacotar o pacote que será recebido pelo medidor, verificar data de fechamento da fatura, fechar fatura, etc.
- Usuario.py: Classe do usuário que possui todas as suas informações.
- Constantes.py: Constantes para padronização do projeto

#### Rotas
Quase todas as requisições são controladas por parâmetros de consulta, que são o par chave-valor que vem após a interrogação (?) depois do endpoint. Os principais parâmetros de consulta são:
- id=value --> value = 1,2,3,...
- mes=value --> value = 01,02,03,...,12
- data=value --> value = 01/01/2001 ou 01/01/ (precisa obrigatoriamente seguir esses formatos)
- horario=value -->  value = 00:00:00 ou 00:00: (precisa obrigatoriamente seguir esses formatos)
##### Requisições GET
Parâmetros de consulta para o usuário de id=1. Para ver outro usuário basta alterar o valor do id. Para o mês, basta alterar entre um valor de 01 até 12, correspondente a cada mês. Para um horário específico, basta deixar no formato HH:MM:, que assim pegará a hora e os minutos específicos.
- Para ver os dados de um determinado usuário: 
```console
/usuario/?id=1
```
- Para ver a fatura de um determinado usuário para um determinado mês: /usuario/fatura/?id=1&mes=01
```console
/usuario/fatura/?id=1&mes=01
```
- Para ver todos os dados de consumo disponíveis: /usuario/consumo/?id=1
```console
/usuario/consumo/?id=1
```
- Para ver os dados de consumo de uma data específica: /usuario/consumo/data/?id=1&data=2023-03-20
```console
/usuario/consumo/data/?id=1&data=2023-03-20
```
- Para ver os dados de consumo de uma data e horário específicos: /usuario/consumo/horario/?id=1&data=2023-03-20&horario=14:10:
```console
/usuario/consumo/horario/?id=1&data=2023-03-20&horario=14:10:
```
- Para ver se há algum alerta de de grande variação: /usuario/alerta/variacao/?id=1
```console
/usuario/alerta/variacao/?id=1
```
- Para ver se há algum alerta de consumo excessivo: /usuario/alerta/excesso/?id=1
```console
/usuario/alerta/excesso/?id=1
```

##### Requisições POST
- Para cadastro de usuário:
```console
/usuario/cadastro/
```
Com o corpo no seguinte formato:
```console
{
    "id": 3,
    "nome": "vitor",
    "endereco": "rua c"
}
```
##### Requisições DELETE
- Para exclusão de usuário:
```console
/usuario/delete/?id=1
```

#### Instruções para executar o código
1. Apenas executar
#### Dockerfile
O Dockerfile possui a seguinte estrutura:
```console
FROM python:3.11-slim-buster
WORKDIR /app
COPY .. /app
EXPOSE 15000
CMD ["python3", "Servidor.py"]
```

- Comando para build da imagem:
```console
docker build -t lpaivao/p1server .
```
- Comando para pull da imagem:
```console
docker pull lpaivao/p1server:latest
```
- Comando para run da imagem:
```console
docker run -p 15000:15000 18000:18000 lpaivao/p1server:latest
```
### Medidor

- Medidor.py: Arquivo principal onde está o socket UDP para comunicação entre o medidor e o servidor. A cada 5 segundos é enviada uma tupla com o seguinte formato: (id do cliente associado ao medidor, data em formato timestamp, consumo acumulado da energia), dados esses que serão empacotados por uma função e enviados imediatamente.
- Funcoes.py: Mesma utilidade do arquivo de mesmo nome do servidor.
- Constantes.py: Mesma utilidade do arquivo de mesmo nome do servidor.

#### Instruções para executar o código
1. Digitar qual o número de id do cliente que será associado ao medidor

#### Dockerfile
```console
FROM python:3.11-slim-buster
WORKDIR /app
COPY .. /app
EXPOSE 18000
CMD ["python3", "Medidor.py"]
```
- Comando para build da imagem:
```console
docker build -t lpaivao/p1med .
```
- Comando para pull da imagem:
```console
docker pull lpaivao/p1med:latest
```
- Comando para run da imagem:
```console
docker run -p 18000:18000 lpaivao/p1med:latest
```
