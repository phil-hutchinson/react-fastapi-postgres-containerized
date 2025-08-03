
from fastapi import FastAPI
from api.services import note as note_router
from api.middleware import setup_cors

def create_app():
    app = FastAPI()

    setup_cors(app)
    # OpenTelemetry metrics setup
    from api.otel_setup import setup_otel_metrics
    setup_otel_metrics()
    # OpenTelemetry tracing setup
    from api.otel_setup import setup_otel_tracing
    setup_otel_tracing()
    # OpenTelemetry HTTP instrumentation setup
    from api.otel_setup import setup_otel_http_instrumentation
    setup_otel_http_instrumentation(app)
    
    app.include_router(note_router.router)

    @app.get("/")
    def read_root():
        return {"message": "Hello from FastAPI + Postgres!"}

    @app.get("/test")
    def test_endpoint():
        return {"status": "ok", "message": "Test endpoint is working!"}

    return app

app = create_app()
