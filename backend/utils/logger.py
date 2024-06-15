import logging
import os
from logging.handlers import TimedRotatingFileHandler

from rich.logging import RichHandler

logger = logging.getLogger(__name__)

log_dir = os.path.join(os.path.normpath(
    os.getcwd() + os.sep + os.pardir), 'logs')
log_fname = os.path.join(log_dir, 'logger.log')

if not os.path.exists(log_dir):
    os.mkdir(log_dir)

# shell_handler = logging.StreamHandler()
shell_handler = RichHandler()
file_handler = TimedRotatingFileHandler(
    log_fname.strip('.'),  when='midnight', backupCount=30)
file_handler.suffix = r'%Y-%m-%d-%H-%M-%S.log'

logger.setLevel(logging.DEBUG)
shell_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)


# the formatter determines what our logs will look like
# fmt_shell = '%(levelname)s %(asctime)s %(message)s'
fmt_shell = '%(message)s'
fmt_file = '%(levelname)4s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'

shell_formatter = logging.Formatter(fmt_shell)
file_formatter = logging.Formatter(fmt_file)

# here we hook everything together
shell_handler.setFormatter(shell_formatter)
file_handler.setFormatter(file_formatter)

logger.addHandler(shell_handler)
logger.addHandler(file_handler)


import time
from typing import Tuple

from opentelemetry import trace
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
#     OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Match
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.types import ASGIApp

# pip3 install opentelemetry-exporter-richconsole
# pip3 install opentelemetry-instrumentation-fastapi
# pip3 install opentelemetry-instrumentation-logging

def setting_otlp(app: ASGIApp, app_name: str, log_correlation: bool = True) -> None: #setting_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)
    # Setting OpenTelemetry
    # set the service name to show in traces
    resource = Resource.create(attributes={
        "service.name": app_name,
        "compose_service": app_name
    })

    # set the tracer provider
    tracer = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer)

    # tracer.add_span_processor(BatchSpanProcessor(
    #     OTLPSpanExporter(endpoint=endpoint)))

    if log_correlation:
        LoggingInstrumentor().instrument(set_logging_format=True)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)