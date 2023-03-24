# Consumo de energia inteligente - Problema 1

- Aluno: Lucas de Paiva Carianha

Desenvolvimento de um protótipo em que os dados serão agregrados visando monitorar o consumo excessivo de energia, medir o consumo de cada cliente, gerar a fatura a ser paga, bem como alertar sobre um possível consumo excessivo de energia ou grande variação na conta de um usuário. Também, os usuários do serviço podem acessar o sistema de forma online para acompanhar o consumo de energia, com datas/horários específicos do consumo e o total acumulado.

## Produto
Os seguintes requisitos do problema foram atendidos:

- [x] Medir o consumo de cada cliente
- [x] Gerar a fatura a ser paga
- [x] Alertar sobre consumo excessivo
- [x] Alertar sobre grande variação
- [x] Acompanhar o consumo de energia com datas/horários específicos
- [x] Visualizar o total acumulado
- [x] Projeto executando no Portainer

O produto está dividido em dois módulos:
- Módulo do servidor
- Módulo do medidor

### Servidor

- Servidor.py: Arquivo principal onde estão os sockets para a comunicação entre cliente-servidor-medidor. Possui dois sockets principais: um socket TCP que escuta as requisições do cliente, e um socket UDP que escuta as informações enviadas do medidor.
- HttpUtils.py: Conjunto de funções utilitárias que tratam as requisições HTTP que serão recebidas pelo servidor principal. Possui, por exemplo, funções para receber requisições GET, POST e DELETE e enviar a resposta de volta para o cliente. Além disso, possui uma função que divide a requisição/resposta HTTP em vários pedaços diferentes e retorna essas partes.
- Funcoes.py: Possui algumas funções mais genéricas com objetivos como: desempacotar o pacote que será recebido pelo medidor, verificar data de fechamento da fatura, fechar fatura, etc.
- Usuario.py: Classe do usuário que possui todas as suas informações.
- Constantes.py: Constantes para padronização do projeto

#### HOST e PORTAS

- O servidor está configurado para escutar/responder os dados em:
```console1
UDP_PORT = 18000
TCP_PORT = 15000
HOST = socket.gethostbyname(socket.gethostname())
```

#### Rotas
Quase todas as requisições são controladas por parâmetros de consulta, que são o par chave-valor que vem após a interrogação (?) depois do endpoint. Os principais parâmetros de consulta são:
- id=value --> value = 1,2,3,...
- mes=value --> value = 01,02,03,...,12
- data=value --> value = 01/01/2001 ou 01/01/ (precisa obrigatoriamente seguir esses formatos)
- horario=value -->  value = 00:00:00 ou :00:00: (precisa obrigatoriamente seguir esses formatos)
##### Requisições GET
- Parâmetros de consulta para o usuário de id=1.
  - Para ver outro usuário basta alterar o valor do id para algum inteiro. 
  - Para o mês, basta alterar entre um valor de 01 até 12, correspondente a cada mês. 
  - Para um horário específico, basta deixar no formato HH:MM: (para o minuto específico de certa hora)
- Para ver os dados de um determinado usuário: 
```console
/usuario/?id=1
```
- Para ver a fatura de um determinado usuário para um determinado mês:
```console
/usuario/fatura/?id=1&mes=01
```
- Para ver todos os dados de consumo disponíveis:
```console
/usuario/consumo/?id=1
```
- Para ver os dados de consumo de uma data específica:
```console
/usuario/consumo/data/?id=1&data=2023-03-20
```
- Para ver os dados de consumo de uma data e horário específicos:
```console
/usuario/consumo/horario/?id=1&data=2023-03-20&horario=14:10:
```
- Para ver se há algum alerta de de grande variação:
```console
/usuario/alerta/variacao/?id=1
```
- Para ver se há algum alerta de consumo excessivo:
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
WORKDIR /Servidor
COPY .. /Servidor
CMD ["python3", "Servidor.py"]
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

#### HOST e PORTA

- Os medidores estão configurados para enviar os dados em:
```console
HOST = "172.16.103.12" (máquina 12 do LARSID)
UDP_PORT = 18000
```

#### Instruções para executar o código do medidor
- Código automático:
  1. Apenas executar, pois, cada imagem do container possui um id[1-4] associado ao medidor.
- Código com entrada do id do cliente e controle de consumo:
  1. Digitar o número do medidor associado ao cliente
  2. Controlar o consumo através de menu iterativo
#### Dockerfile
```console
FROM python:3.11-slim-buster
WORKDIR /Medidor
COPY .. /Medidor
CMD ["python3", "Medidor.py"]
```
- Comando para pull da imagem dos três medidores automáiticos:
```console
docker pull lpaivao/p1med:auto1  ## Medidor associado ao cliente 1
docker pull lpaivao/p1med:auto2  ## Medidor associado ao cliente 2
docker pull lpaivao/p1med:auto3  ## Medidor associado ao cliente 3
docker pull lpaivao/p1med:auto4  ## Medidor associado ao cliente 4
```
- Comando para run da imagem:
```console
docker run -p lpaivao/p1med:auto1
docker run -p lpaivao/p1med:auto2
docker run -p lpaivao/p1med:auto3
docker run -p lpaivao/p1med:auto4
```
