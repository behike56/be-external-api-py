from http import HTTPStatus as sTs
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import src.api.cruds.done as done_crud
import src.api.schemas.done as done_schema
from src.api.db import get_db

router = APIRouter()


@router.put("/tasks/{task_id}/done", response_model=done_schema.DoneResponse)
async def mark_task_as_done(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> done_schema.DoneResponse:
    done = await done_crud.get_done(db, task_id)
    if done is not None:
        raise HTTPException(status_code=sTs.BAD_REQUEST, detail="Done already exists")

    return await done_crud.create_done(db, task_id)


@router.delete("/tasks/{task_id}/done", response_model=None)
async def unmark_task_as_done(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    done = await done_crud.get_done(db, task_id)
    if done is None:
        raise HTTPException(status_code=sTs.NOT_FOUND, detail="Done not found")

    return await done_crud.delete_done(db, original=done)
