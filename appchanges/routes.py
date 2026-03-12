from flask import render_template


def register_routes(app):

    @app.get("/")
    def home():
        return render_template("index.html")