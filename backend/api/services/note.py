from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.note import Note
from api.schemas.note import NoteCreate, NoteSummary, NoteDetail, NoteUpdate
from api.database import get_db
from typing import List

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteDetail)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = Note(name=note.name, description=note.description)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return {"uuid": str(db_note.uuid), "name": db_note.name, "description": db_note.description, "finalized": db_note.finalized}

@router.get("/", response_model=List[NoteSummary])
def list_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).order_by(Note.id.asc()).all()
    return [{"uuid": str(e.uuid), "name": e.name} for e in notes]

@router.get("/{uuid}", response_model=NoteDetail)
def get_note_detail(uuid: str, db: Session = Depends(get_db)):
    note = db.query(Note).filter_by(uuid=uuid).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"uuid": str(note.uuid), "name": note.name, "description": note.description, "finalized": note.finalized}

@router.put("/{uuid}", response_model=NoteDetail)
def update_note(uuid: str, update: NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(Note).filter_by(uuid=uuid).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.finalized:
        raise HTTPException(status_code=409, detail="Note is locked and cannot be modified.")
    if update.name is not None:
        note.name = update.name
    if update.description is not None:
        note.description = update.description
    db.commit()
    db.refresh(note)
    return {"uuid": str(note.uuid), "name": note.name, "description": note.description, "finalized": note.finalized}

@router.put("/{uuid}/lock", response_model=NoteDetail)
def lock_note(uuid: str, db: Session = Depends(get_db)):
    note = db.query(Note).filter_by(uuid=uuid).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.finalized:
        raise HTTPException(status_code=409, detail="Note is already locked.")
    note.finalized = True
    db.commit()
    db.refresh(note)
    return {"uuid": str(note.uuid), "name": note.name, "description": note.description, "finalized": note.finalized}

@router.delete("/{uuid}", response_model=dict)
def delete_note(uuid: str, db: Session = Depends(get_db)):
    note = db.query(Note).filter_by(uuid=uuid).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.finalized:
        raise HTTPException(status_code=409, detail="Note is locked and cannot be deleted.")
    db.delete(note)
    db.commit()
    return {"detail": "Note deleted"}
