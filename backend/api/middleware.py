
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

def setup_cors(app):
    """
    Adds CORS middleware to the FastAPI app.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def setup_metrics(app):
    """
    Adds Prometheus metrics middleware to the FastAPI app.
    """
    Instrumentator().instrument(app).expose(app)
