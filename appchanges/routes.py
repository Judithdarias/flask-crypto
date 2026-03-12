from flask import render_template
from appchanges.model import ModelCrypto

model = ModelCrypto()


def register_routes(app):

    @app.get("/")
    def home():
        model.get_all_movimientos()
        return render_template("index.html", movimientos=model.movimientos)

    @app.get("/purchase")
    def purchase():
        return render_template("purchase.html")

    @app.get("/status")
    def status():
        return render_template("status.html")

