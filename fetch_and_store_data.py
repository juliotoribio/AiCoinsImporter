import requests
from datetime import datetime
import mysql.connector
from dateutil import parser

def get_db_connection():
    conn = mysql.connector.connect(
        host='monorail.proxy.rlwy.net',
        user='root',
        password='HfFASSAcXEvaTMcdQofTiWRNPhksVqHn',
        database='railway',
        port=20944
    )
    return conn

def fetch_and_store_data():
    api_key = '65653bd8-ed89-4111-9523-a66a136cd9cc'
    categoria_id = '6051a81a66fc1b42617d6db7'
    limite_por_pagina = 1000
    seguir_importando = True
    start = 1

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM crypto_data;')

    while seguir_importando:
        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/category?id={categoria_id}&limit={limite_por_pagina}&start={start}'
        headers = {'X-CMC_PRO_API_KEY': api_key, 'Accept': 'application/json'}
        respuesta = requests.get(url, headers=headers)
        datos = respuesta.json().get('data')

        if datos and datos['coins']:
            for coin in datos['coins']:
                last_updated = parser.parse(coin['last_updated']).strftime('%Y-%m-%d %H:%M:%S')
                cur.execute('''
                    INSERT INTO crypto_data (id, name, symbol, slug, price, market_cap, volume_24h, circulating_supply, percent_change_1h, percent_change_24h, percent_change_7d, cmc_rank, last_updated, import_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    coin['id'],
                    coin['name'],
                    coin['symbol'],
                    coin['slug'],
                    coin['quote']['USD']['price'],
                    coin['quote']['USD']['market_cap'],
                    coin['quote']['USD']['volume_24h'],
                    coin['circulating_supply'],
                    coin['quote']['USD']['percent_change_1h'],
                    coin['quote']['USD']['percent_change_24h'],
                    coin['quote']['USD']['percent_change_7d'],
                    coin['cmc_rank'],
                    last_updated,
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Añade la fecha de importación
                ))
            start += limite_por_pagina
        else:
            seguir_importando = False

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    fetch_and_store_data()
