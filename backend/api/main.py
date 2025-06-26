from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.services import example as example_router

def create_app():
    app = FastAPI()

    # Allow CORS for all origins (development only)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(example_router.router)

    @app.get("/")
    def read_root():
        return {"message": "Hello from FastAPI + Postgres!"}

    @app.get("/test")
    def test_endpoint():
        return {"status": "ok", "message": "Test endpoint is working!"}

    return app

app = create_app()
