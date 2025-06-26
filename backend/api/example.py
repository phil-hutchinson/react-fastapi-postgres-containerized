from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.example import Example
from api.schemas.example import ExampleCreate, ExampleSummary, ExampleDetail, ExampleUpdate
from .database import get_db
from typing import List

router = APIRouter(prefix="/examples", tags=["examples"])

@router.post("/", response_model=ExampleDetail)
def create_example(example: ExampleCreate, db: Session = Depends(get_db)):
    db_example = Example(name=example.name, description=example.description)
    db.add(db_example)
    db.commit()
    db.refresh(db_example)
    return {"uuid": str(db_example.uuid), "name": db_example.name, "description": db_example.description}

@router.get("/", response_model=List[ExampleSummary])
def list_examples(db: Session = Depends(get_db)):
    examples = db.query(Example).all()
    return [{"uuid": str(e.uuid), "name": e.name} for e in examples]

@router.get("/{uuid}", response_model=ExampleDetail)
def get_example_detail(uuid: str, db: Session = Depends(get_db)):
    example = db.query(Example).filter_by(uuid=uuid).first()
    if not example:
        raise HTTPException(status_code=404, detail="Example not found")
    return {"uuid": str(example.uuid), "name": example.name, "description": example.description}

@router.put("/{uuid}", response_model=ExampleDetail)
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
