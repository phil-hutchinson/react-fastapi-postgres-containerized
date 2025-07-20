from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry import metrics

def setup_otel_metrics():
    otlp_exporter = OTLPMetricExporter(endpoint="http://otel-collector:4318/v1/metrics")
    reader = PeriodicExportingMetricReader(otlp_exporter)
    provider = MeterProvider(metric_readers=[reader])
    metrics.set_meter_provider(provider)
