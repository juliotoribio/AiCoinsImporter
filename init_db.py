import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host='monorail.proxy.rlwy.net',
        user='root',
        password='HfFASSAcXEvaTMcdQofTiWRNPhksVqHn',
        database='railway',
        port=20944
    )
    return conn

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS crypto_data (
            id INT PRIMARY KEY,
            name VARCHAR(255),
            symbol VARCHAR(50),
            slug VARCHAR(255),
            price DECIMAL(20, 10),
            market_cap DECIMAL(20, 2),
            volume_24h DECIMAL(20, 2),
            circulating_supply DECIMAL(20, 2),
            percent_change_1h DECIMAL(10, 2),
            percent_change_24h DECIMAL(10, 2),
            percent_change_7d DECIMAL(10, 2),
            cmc_rank INT,
            last_updated DATETIME,
            import_date DATETIME,
            snapshot DATETIME
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_tables()
