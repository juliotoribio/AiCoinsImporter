from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host='monorail.proxy.rlwy.net',
        user='root',
        password='HfFASSAcXEvaTMcdQofTiWRNPhksVqHn',
        database='railway',
        port=20944
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, symbol, price, market_cap, volume_24h, cmc_rank, last_updated, import_date FROM crypto_data;')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
