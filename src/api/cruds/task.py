from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.engine import Result

import src.api.models.task as task_model
import src.api.schemas.task as task_schema


def create_task(db: Session, task_create: task_schema.TaskCreate) -> task_model.Task:
    """タスクを作成する
    Args:
        db: Session: データベースセッション
        task_create: TaskCreate: 作成するタスクの情報
    Returns:
        Task: 作成したタスク
    """
    task = task_model.Task(**task_create.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks_with_done(db: Session) -> list[tuple[int, str, bool]]:
    """完了済みのタスクを取得する
    Args:
        db: Session: データベースセッション
    Returns:
        list[tuple[int, str, bool]]: 完了済みのタスクのリスト
    """
    # Result型はイテレータ。この時点ではまだ全ての結果が入っていない。
    result: Result = db.execute(
        select(
            task_model.Task.id,
            task_model.Task.title,
            task_model.Done.id.isnot(None).label("done"),
        ).outerjoin(task_model.Done)
    )

    return result.all()


def get_task(db: Session, task_id: int) -> task_model.Task | None:
    result: Result = db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    return result.scalars().first()


def update_task(
    db: Session, task_create: task_schema.TaskCreate, original: task_model.Task
) -> task_model.Task:
    original.title = task_create.title
    db.add(original)
    db.commit()
    db.refresh(original)
    return original

def delete_task(db: Session, original: task_model.Task) -> None:
    db.delete(original)
    db.commit()
