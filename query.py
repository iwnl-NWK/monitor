#!/usr/bin/python3
from influxdb_client import InfluxDBClient

# --- Configurações da Conexão ---
url = "http://localhost:8086"
token = "senha" # O mesmo token do docker-compose
org = "esp32_org"
bucket = "health_data"

# --- Cliente InfluxDB ---
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

# --- Escreva sua query em Flux ---
flux_query = f'''
from(bucket: "{bucket}")
  |> range(start: -10m) // Pega os dados dos últimos 10 minutos
  |> filter(fn: (r) => r._measurement == "health_metrics")
'''

# --- Execute a query ---
tables = query_api.query(flux_query)

# --- Processe os resultados ---
if not tables:
    print("Nenhum dado de BPM encontrado nos últimos 10 minutos.")
else:
    for table in tables:
        for record in table.records:
            print(f"Último BPM registrado: {record.get_value()} em {record.get_time()}")

client.close()
