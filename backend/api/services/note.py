from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.note import Note
from api.schemas.note import NoteCreate, NoteSummary, NoteDetail, NoteUpdate
from api.database import get_db
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteDetail)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new note with name: {note.name}")
    try:
        db_note = Note(name=note.name, description=note.description)
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        logger.info(f"Successfully created note with UUID: {db_note.uuid}")
        return {"uuid": str(db_note.uuid), "name": db_note.name, "description": db_note.description, "locked": db_note.locked}
    except SQLAlchemyError as e:
        logger.error(f"Database error while creating note: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error while creating note: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[NoteSummary])
def list_notes(db: Session = Depends(get_db)):
    logger.info("Fetching all notes")
    try:
        notes = db.query(Note).order_by(Note.id.asc()).all()
        logger.info(f"Successfully retrieved {len(notes)} notes")
        return [{"uuid": str(e.uuid), "name": e.name} for e in notes]
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching notes: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error while fetching notes: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{uuid}", response_model=NoteDetail)
def get_note_detail(uuid: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching note details for UUID: {uuid}")
    try:
        note = db.query(Note).filter_by(uuid=uuid).first()
        if not note:
            logger.warning(f"Note not found for UUID: {uuid}")
            raise HTTPException(status_code=404, detail="Note not found")
        logger.info(f"Successfully retrieved note: {note.name}")
        return {"uuid": str(note.uuid), "name": note.name, "description": note.description, "locked": note.locked}
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching note {uuid}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error while fetching note {uuid}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{uuid}", response_model=NoteDetail)
def update_note(uuid: str, update: NoteUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating note with UUID: {uuid}")
    try:
        note = db.query(Note).filter_by(uuid=uuid).first()
        if not note:
            logger.warning(f"Note not found for update, UUID: {uuid}")
            raise HTTPException(status_code=404, detail="Note not found")
        if note.locked:
            logger.warning(f"Attempted to update locked note: {uuid}")
            raise HTTPException(status_code=409, detail="Note is locked and cannot be modified.")
        
        if update.name is not None:
            note.name = update.name
        if update.description is not None:
            note.description = update.description
        db.commit()
        db.refresh(note)
        logger.info(f"Successfully updated note: {note.name}")
        return {"uuid": str(note.uuid), "name": note.name, "description": note.description, "locked": note.locked}
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except SQLAlchemyError as e:
        logger.error(f"Database error while updating note {uuid}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error while updating note {uuid}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{uuid}/lock", response_model=NoteDetail)
def lock_note(uuid: str, db: Session = Depends(get_db)):
    logger.info(f"Locking note with UUID: {uuid}")
    try:
        note = db.query(Note).filter_by(uuid=uuid).first()
        if not note:
            logger.warning(f"Note not found for locking, UUID: {uuid}")
            raise HTTPException(status_code=404, detail="Note not found")
        if note.locked:
            logger.warning(f"Attempted to lock already locked note: {uuid}")
            raise HTTPException(status_code=409, detail="Note is already locked.")
        
        note.locked = True
        db.commit()
        db.refresh(note)
        logger.info(f"Successfully locked note: {note.name}")
        return {"uuid": str(note.uuid), "name": note.name, "description": note.description, "locked": note.locked}
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except SQLAlchemyError as e:
        logger.error(f"Database error while locking note {uuid}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error while locking note {uuid}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{uuid}", response_model=dict)
def delete_note(uuid: str, db: Session = Depends(get_db)):
    logger.info(f"Deleting note with UUID: {uuid}")
    try:
        note = db.query(Note).filter_by(uuid=uuid).first()
        if not note:
            logger.warning(f"Note not found for deletion, UUID: {uuid}")
            raise HTTPException(status_code=404, detail="Note not found")
        if note.locked:
            logger.warning(f"Attempted to delete locked note: {uuid}")
            raise HTTPException(status_code=409, detail="Note is locked and cannot be deleted.")
        
        note_name = note.name  # Store name for logging before deletion
        db.delete(note)
        db.commit()
        logger.info(f"Successfully deleted note: {note_name}")
        return {"detail": "Note deleted"}
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except SQLAlchemyError as e:
        logger.error(f"Database error while deleting note {uuid}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error while deleting note {uuid}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
