from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from models import Base
from models.example import Example
from pydantic import BaseModel
from typing import List

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Allow CORS for all origins (development only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ExampleCreate(BaseModel):
    name: str
    description: str | None = None

class ExampleSummary(BaseModel):
    uuid: str
    name: str

class ExampleDetail(BaseModel):
    uuid: str
    name: str
    description: str | None = None

class ExampleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

@app.post("/examples", response_model=dict)
def create_example(example: ExampleCreate, db: Session = Depends(get_db)):
    db_example = Example(name=example.name, description=example.description)
    db.add(db_example)
    db.commit()
    db.refresh(db_example)
    return {"id": db_example.id, "uuid": str(db_example.uuid), "name": db_example.name, "description": db_example.description}

@app.get("/examples", response_model=List[ExampleSummary])
def list_examples(db: Session = Depends(get_db)):
    examples = db.query(Example).all()
    return [{"uuid": str(e.uuid), "name": e.name} for e in examples]

@app.get("/examples/{uuid}", response_model=ExampleDetail)
def get_example_detail(uuid: str, db: Session = Depends(get_db)):
    example = db.query(Example).filter_by(uuid=uuid).first()
    if not example:
        raise HTTPException(status_code=404, detail="Example not found")
    return {"uuid": str(example.uuid), "name": example.name, "description": example.description}

@app.put("/examples/{uuid}", response_model=ExampleDetail)
def update_example(uuid: str, update: ExampleUpdate, db: Session = Depends(get_db)):
    example = db.query(Example).filter_by(uuid=uuid).first()
    if not example:
        raise HTTPException(status_code=404, detail="Example not found")
    if update.name is not None:
        example.name = update.name
    if update.description is not None:
        example.description = update.description
    db.commit()
    db.refresh(example)
    return {"uuid": str(example.uuid), "name": example.name, "description": example.description}

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + Postgres!"}

@app.get("/test")
def test_endpoint():
    return {"status": "ok", "message": "Test endpoint is working!"}
