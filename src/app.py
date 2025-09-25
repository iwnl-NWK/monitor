from flask import Flask, render_template, jsonify
from influxdb_client import InfluxDBClient
import os

app = Flask(__name__)

INFLUXDB_URL = os.environ.get("INFLUXDB_URL")
INFLUXDB_TOKEN = os.environ.get("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.environ.get("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.environ.get("INFLUXDB_BUCKET")

@app.route('/')
def index():
    """Serve a página principal do dashboard."""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """API que busca os dados históricos do InfluxDB para popular o gráfico."""
    try:
        client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        query_api = client.query_api()

        # Query Flux para buscar os últimos 100 pontos de cada métrica
        flux_query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
          |> range(start: -1h)
          |> filter(fn: (r) => r._measurement == "health_metrics")
          |> filter(fn: (r) => r._field == "bpm_value" or r._field == "spo2_value" or r._field == "ecg_value")
          |> limit(n: 100)
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        '''
        
        tables = query_api.query(flux_query)
        
        results = {
            "labels": [],
            "ecg": [],
            "bpm": [],
            "spo2": []
        }
        
        for table in tables:
            for record in table.records:
                results["labels"].append(record.get_time().isoformat())
                results["ecg"].append(record.get_value_by_key("ecg_value"))
                results["bpm"].append(record.get_value_by_key("bpm_value"))
                results["spo2"].append(record.get_value_by_key("spo2_value"))

        return jsonify(results)

    except Exception as e:
        print(f"Erro ao conectar ou buscar dados do InfluxDB: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
