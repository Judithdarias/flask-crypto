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
