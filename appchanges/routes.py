from flask import render_template


def register_routes(app):

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/purchase")
    def purchase():
        return render_template("purchase.html")

    @app.get("/status")
    def status():
        return render_template("status.html")
