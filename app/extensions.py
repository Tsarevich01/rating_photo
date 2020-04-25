from sanic import Sanic
from database import db

from sanic_cors import CORS

from .helpers import trace


def register_db(app: Sanic):
    app.config.DB_DSN = app.config.PG_CONNECTION
    app.config.DB_ECHO = app.config.DEBUG
    db.init_app(app)
    app.db = db


def register_async_helpers(app: Sanic):
    app.run_in_executor = trace.run_in_executor
    app.gather_in_executor = trace.gather_in_executor
    app.gather = trace.gather
    app.create_task = trace.create_task


def register_cors(app: Sanic):
    app.cors = CORS(app)
