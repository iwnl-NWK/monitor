# Projeto de Monitoramento de sinais vitais utilizando ESP32

## Este repositório abriga os arquivos necessários para executar o MQTT Broker, Página de monitoramento e o coletor de dados.

### Tecnologias usadas:
 - [Docker](https://www.docker.com/get-started)
 - [Telegraf](https://github.com/influxdata/telegraf)
 - [InfluxDB](https://github.com/influxdata/influxdb)
 - [Mosquitto Broker](https://mosquitto-org.translate.goog/?_x_tr_sl=en&_x_tr_tl=pt&_x_tr_hl=pt&_x_tr_pto=tc)
 - [Paho Client](https://github.com/eclipse-paho/paho.mqtt.c)

## Executando o projeto:

```Bash
git clone https://github.com/iwnl-NWK/monitor.git
cd monitor
docker-compose up --build -d
```

> **Importante**: certifique-se de instalar docker/docker-compose para executar o projeto

## Checar os dados:

caso queira checar os dados dos tópicos sendo importados pelo coletor, é possível utilizar o script **query.py**:

```bash
cd monitor
python3 query.py
``` 

> Exemplo utilizando Ubuntu 22.04, adapte para o seu ambiente

### Checando so dados do monitoramento:


utilizando o navegador, acesse a url:

```bash
# se estiver executando o projeto no mesmo dispositivo que irá utilizar para o monitoramento
http://localhost

# para acesso remoto:
http://<IP | FQDN do servidor executando o projeto>
```
