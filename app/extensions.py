from sanic import Sanic
from database import db

from app import jwt
from sanic_cors import CORS
from ddtrace import tracer
from ddtrace.contrib.asyncio import context_provider
from ddtrace.contrib.logging import patch as ddtrace_logging_patch

from .helpers import password_hasher, trace


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


def register_ddtrace(app: Sanic):
    ddtrace_logging_patch()
    if app.config.IS_DOCKER:
        app.config.DDTARCE_HOSTNAME = app.config.DEFAULT_GATEWAY
    tracer.configure(hostname=app.config.DDTARCE_HOSTNAME, context_provider=context_provider)
    app.register_middleware(trace.ddtarce_on_request, 'request')
    app.register_middleware(trace.ddtarce_on_response, 'response')


def register_cors(app: Sanic):
    app.cors = CORS(app)
