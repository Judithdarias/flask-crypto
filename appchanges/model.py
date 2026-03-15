import requests
from appchanges.config import API_KEY, BASE_URL
from appchanges.db import get_connection


class ModelCrypto:
    def __init__(self):
        self.movimientos = []

    def get_all_movimientos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT date, time, moneda_from, cantidad_from, moneda_to, cantidad_to
            FROM movimientos
            ORDER BY date DESC, time DESC
        """)

        filas = cursor.fetchall()
        conn.close()

        self.movimientos = filas
        
    def calcular_conversion(self, cantidad_from, moneda_from, moneda_to):
        headers = {
            "X-CMC_PRO_API_KEY": API_KEY,
            "Accept": "application/json"
        }

        params = {
            "amount": cantidad_from,
            "symbol": moneda_from,
            "convert": moneda_to
        }

        response = requests.get(
            f"{BASE_URL}/v2/tools/price-conversion",
            headers=headers,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            raise Exception("Error al consultar la API de CoinMarketCap")

        data = response.json()

        try:
            cantidad_to = data["data"][0]["quote"][moneda_to]["price"]
        except:
            raise Exception("No se pudo calcular la conversión")

        return round(cantidad_to, 8)



    def insert_movimiento(self, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO movimientos (
                date, time, moneda_from, cantidad_from, moneda_to, cantidad_to
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to))

        conn.commit()
        conn.close()

    def get_resumen_inversion(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(cantidad_from) 
            FROM movimientos
            WHERE moneda_from = 'EUR'
        """)
        invertido = cursor.fetchone()[0]

        cursor.execute("""
            SELECT SUM(cantidad_to)
            FROM movimientos
            WHERE moneda_to = 'EUR'
        """)
        recuperado = cursor.fetchone()[0]

        conn.close()

        if invertido is None:
            invertido = 0

        if recuperado is None:
            recuperado = 0

        valor_compra = invertido - recuperado

        return {
            "invertido": invertido,
            "recuperado": recuperado,
            "valor_compra": valor_compra
        }

    def get_saldos_monedas(self):
        monedas = ["BTC", "ETH", "USDT", "BNB", "XRP", "ADA", "SOL", "DOT", "MATIC"]
        saldos = {}

        conn = get_connection()
        cursor = conn.cursor()

        for moneda in monedas:
            cursor.execute("""
                SELECT SUM(cantidad_to)
                FROM movimientos
                WHERE moneda_to = ?
            """, (moneda,))
            entradas = cursor.fetchone()[0]

            cursor.execute("""
                SELECT SUM(cantidad_from)
                FROM movimientos
                WHERE moneda_from = ?
            """, (moneda,))
            salidas = cursor.fetchone()[0]

            if entradas is None:
                entradas = 0

            if salidas is None:
                salidas = 0

            saldo = entradas - salidas

            if saldo > 0:
                saldos[moneda] = saldo

        conn.close()

        return saldos
