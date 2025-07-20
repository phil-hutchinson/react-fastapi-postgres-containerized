
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from models.base import Base

# OpenTelemetry SQLAlchemy instrumentation
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Instrument SQLAlchemy engine
SQLAlchemyInstrumentor().instrument(engine=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
