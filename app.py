import os
import requests
import psycopg2
import pandas as pd
from flask import Flask, render_template
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Establecer la URL de conexión de la base de datos
DATABASE_URL = "postgresql://postgres:VWcHHVyjoQJCZGXbufNAKOYwVRDTcNof@viaduct.proxy.rlwy.net:35174/railway"
API_KEY = 'tu_api_key_aqui'
API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

def fetch_and_store_data():
    response = requests.get(API_URL, headers=headers)
    data = response.json()

    if 'data' in data:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        
        for crypto in data['data']:
            name = crypto['name']
            symbol = crypto['symbol']
            price_usd = crypto['quote']['USD']['price']
            market_cap_usd = crypto['quote']['USD']['market_cap']
            last_updated = crypto['last_updated']

            cursor.execute('''
            INSERT INTO prices (name, symbol, price_usd, market_cap_usd, last_updated)
            VALUES (%s, %s, %s, %s, %s)
            ''', (name, symbol, price_usd, market_cap_usd, last_updated))
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Datos guardados exitosamente.")
    else:
        print("Error al obtener datos:", data)

@app.route('/')
def index():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    df = pd.read_sql_query('SELECT * FROM prices', conn)
    conn.close()

    average_price = df['price_usd'].mean()
    return render_template('index.html', tables=[df.to_html(classes='data')], average_price=average_price)

if __name__ == '__main__':
    app.run(debug=True)
