
from fastapi import FastAPI
from api.services import note as note_router
from api.services import simulation as simulation_router
from api.middleware import setup_cors
import logging

logger = logging.getLogger(__name__)

def create_app():
    app = FastAPI(
        root_path="/api"  # Set root path for reverse proxy
    )

    setup_cors(app)
    # OpenTelemetry metrics setup
    from api.otel_setup import setup_otel_metrics
    setup_otel_metrics()
    # OpenTelemetry tracing setup
    from api.otel_setup import setup_otel_tracing
    setup_otel_tracing()
    # OpenTelemetry logging setup
    from api.otel_setup import setup_otel_logging
    setup_otel_logging()
    # OpenTelemetry HTTP instrumentation setup
    from api.otel_setup import setup_otel_http_instrumentation
    setup_otel_http_instrumentation(app)
    
    app.include_router(note_router.router)
    app.include_router(simulation_router.router)

    @app.get("/")
    def read_root():
        logger.info("Root endpoint accessed")
        return {"message": "Hello from FastAPI + Postgres!"}

    @app.get("/test")
    def test_endpoint():
        logger.info("Test endpoint accessed")
        return {"status": "ok", "message": "Test endpoint is working!"}

    return app

app = create_app()
