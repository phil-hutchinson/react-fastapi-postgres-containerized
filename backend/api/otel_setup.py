
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry import metrics

# Tracing imports
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace

# Logging imports
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
import logging

# HTTP instrumentation imports
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_otel_metrics():
    otlp_exporter = OTLPMetricExporter(endpoint="http://otel-collector:4318/v1/metrics")
    reader = PeriodicExportingMetricReader(otlp_exporter)
    provider = MeterProvider(metric_readers=[reader])
    metrics.set_meter_provider(provider)


def setup_otel_tracing():
    trace_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces")
    resource = Resource.create({SERVICE_NAME: "backend"})
    tracer_provider = TracerProvider(resource=resource)
    span_processor = BatchSpanProcessor(trace_exporter)
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)


def setup_otel_logging():
    """
    Sets up OpenTelemetry logging to send logs to the collector.
    This bridges Python's standard logging to OpenTelemetry.
    """
    resource = Resource.create({SERVICE_NAME: "backend"})
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)
    
    # Use gRPC endpoint to match collector configuration
    log_exporter = OTLPLogExporter(endpoint="http://otel-collector:4317", insecure=True)
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(log_exporter)
    )
    
    # Bridge Python's standard logging to OpenTelemetry
    otel_handler = LoggingHandler(logger_provider=logger_provider)
    
    # Configure root logger to send to OpenTelemetry
    root_logger = logging.getLogger()
    root_logger.addHandler(otel_handler)
    root_logger.setLevel(logging.INFO)
    
    # Also configure console logging for development
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    root_logger.addHandler(console_handler)


def setup_otel_http_instrumentation(app):
    """
    Sets up OpenTelemetry HTTP instrumentation for FastAPI.
    This replaces the Prometheus FastAPI Instrumentator.
    """
    FastAPIInstrumentor.instrument_app(app)
