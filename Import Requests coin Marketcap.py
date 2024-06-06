import requests
from datetime import datetime

def mostrar_datos_de_criptomonedas():
    # Configura tu API key y otros parámetros
    api_key = '65653bd8-ed89-4111-9523-a66a136cd9cc'
    categoria_id = '6051a81a66fc1b42617d6db7'
    limite_por_pagina = 1000
    seguir_importando = True
    start = 1

    while seguir_importando:
        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/category?id={categoria_id}&limit={limite_por_pagina}&start={start}'
        headers = {'X-CMC_PRO_API_KEY': api_key, 'Accept': 'application/json'}
        respuesta = requests.get(url, headers=headers)
        datos = respuesta.json().get('data')

        if datos and datos['coins']:
            for coin in datos['coins']:
                print("ID:", coin['id'])
                print("Nombre:", coin['name'])
                print("Símbolo:", coin['symbol'])
                print("Slug:", coin['slug'])
                print("Precio (USD):", coin['quote']['USD']['price'])
                print("Capitalización de Mercado:", coin['quote']['USD']['market_cap'])
                print("Volumen (24h):", coin['quote']['USD']['volume_24h'])
                print("Suministro Circulante:", coin['circulating_supply'])
                print("Cambio Porcentual 1h:", coin['quote']['USD']['percent_change_1h'])
                print("Cambio Porcentual 24h:", coin['quote']['USD']['percent_change_24h'])
                print("Cambio Porcentual 7d:", coin['quote']['USD']['percent_change_7d'])
                print("Ranking CMC:", coin['cmc_rank'])
                print("Última Actualización:", coin['last_updated'])
                print("Fecha de Importación:", datetime.now())
                print("----------------------------")
            start += limite_por_pagina
        else:
            seguir_importando = False

# Llamada a la función principal
mostrar_datos_de_criptomonedas()
