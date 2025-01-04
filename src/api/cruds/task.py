from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

import src.api.models.task as task_model
import src.api.schemas.task as task_schema

if TYPE_CHECKING:
    from sqlalchemy.engine import Result
    from sqlalchemy.ext.asyncio import AsyncSession


async def create_task(
    db: AsyncSession,
    task_create: task_schema.TaskCreate,
) -> task_model.Task:
    """タスクを作成する async.

    Args:
        db: AsyncSession: データベースセッション
        task_create: TaskCreate: 作成するタスクの情報
    Returns:
        Task: 作成したタスク

    """
    task = task_model.Task(**task_create.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_tasks_with_done(db: AsyncSession) -> list[tuple[int, str, bool]]:
    """完了済みのタスクを取得する.

    Args:
        db: Session: データベースセッション
    Returns:
        list[tuple[int, str, bool]]: 完了済みのタスクのリスト

    """
    # Result型はイテレータ。この時点ではまだ全ての結果が入っていない。
    result: Result = await db.execute(
        select(
            task_model.Task.id,
            task_model.Task.title,
            task_model.Done.id.isnot(None).label("done"),
        ).outerjoin(task_model.Done),
    )

    return result.all()


async def get_task(db: AsyncSession, task_id: int) -> task_model.Task | None:
    result: Result = await db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id),
    )
    return result.scalars().first()


async def update_task(
    db: AsyncSession,
    task_create: task_schema.TaskCreate,
    original: task_model.Task,
) -> task_model.Task:
    original.title = task_create.title
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_task(db: AsyncSession, original: task_model.Task) -> None:
    await db.delete(original)
    await db.commit()
