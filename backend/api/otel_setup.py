
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


def setup_otel_http_instrumentation(app):
    """
    Sets up OpenTelemetry HTTP instrumentation for FastAPI.
    This replaces the Prometheus FastAPI Instrumentator.
    """
    FastAPIInstrumentor.instrument_app(app)
