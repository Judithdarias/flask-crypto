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
        
    def calcular_conversion(self, cantidad_from):
        return round(cantidad_from * 2, 8)

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
