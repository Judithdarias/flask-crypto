from datetime import datetime
from flask import render_template, request, redirect
from appchanges.model import ModelCrypto

MONEDAS = ["EUR", "BTC", "ETH", "USDT", "BNB", "XRP", "ADA", "SOL", "DOT", "MATIC"]

model = ModelCrypto()


def register_routes(app):

    @app.get("/")
    def home():
        model.get_all_movimientos()
        return render_template("index.html", movimientos=model.movimientos)

    @app.route("/purchase", methods=["GET", "POST"])
    def purchase():
        if request.method == "GET":
            return render_template(
                "purchase.html",
                monedas=MONEDAS,
                moneda_from="",
                cantidad_from="",
                moneda_to="",
                accion="",
                cantidad_to=""
            )

        moneda_from = request.form.get("moneda_from", "")
        cantidad_from = request.form.get("cantidad_from", "")
        moneda_to = request.form.get("moneda_to", "")
        accion = request.form.get("accion", "")

        if moneda_from == moneda_to:
            return render_template("error.html", message="La moneda origen y destino no pueden ser iguales")

        try:
            cantidad_from_float = float(cantidad_from)
        except:
            return render_template("error.html", message="La cantidad debe ser un número válido")

        if cantidad_from_float <= 0:
            return render_template("error.html", message="La cantidad debe ser mayor que cero")

        try:
            cantidad_to = model.calcular_conversion(cantidad_from_float, moneda_from, moneda_to)
        except Exception as e:
            return render_template("error.html", message=str(e))


        if accion == "aceptar":
            ahora = datetime.now()

            date = ahora.strftime("%Y-%m-%d")
            time = ahora.strftime("%H:%M:%S")

            model.insert_movimiento(
                date,
                time,
                moneda_from,
                cantidad_from_float,
                moneda_to,
                cantidad_to
            )

            return redirect("/")

        return render_template(
            "purchase.html",
            monedas=MONEDAS,
            moneda_from=moneda_from,
            cantidad_from=cantidad_from,
            moneda_to=moneda_to,
            accion=accion,
            cantidad_to=cantidad_to
        )


    @app.get("/status")
    def status():
        resumen = model.get_resumen_inversion()
        saldos = model.get_saldos_monedas()
        return render_template("status.html", resumen=resumen, saldos=saldos)


