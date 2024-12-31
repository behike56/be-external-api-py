from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from http import HTTPStatus as sts
import src.api.cruds.done as done_crud
import src.api.schemas.done as done_schema
from src.db.database import get_db

router = APIRouter()

@router.put("/tasks/{task_id}/done", response_model=done_schema.DoneResponse)
async def mark_task_as_done(task_id: int, db: Session = Depends(get_db)):
    done = done_crud.get_done(db, task_id)
    if done is not None:
        raise HTTPException(status_code=sts.BAD_REQUEST, detail="Done already exists")
    
    return done_crud.create_done(db, task_id)

@router.delete("/tasks/{task_id}/done", response_model=None)
async def unmark_task_as_done(task_id: int, db: Session = Depends(get_db)):
    done = done_crud.get_done(db, task_id)
    if done is None:
        raise HTTPException(status_code=sts.NOT_FOUND, detail="Done not found")
    
    return done_crud.delete_done(db, original=done)