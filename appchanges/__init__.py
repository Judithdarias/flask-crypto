from flask import Flask
from appchanges.routes import register_routes
from appchanges.db import create_tables

app = Flask(__name__)
register_routes(app)
create_tables()
