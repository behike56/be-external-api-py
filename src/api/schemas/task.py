"""タスクのスキーマ"""

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """タスクのベース"""
    title: str | None = Field(None, example="本を返しに行く。")

class Task(TaskBase):
    """タスク"""
    # タスクID
    id: int
    # 完了フラグ
    done: bool = Field(False, description="完了フラグ")
    
    class Config:
        # モデルのデータを辞書に変換する(IMPLICIT)
        orm_mode = True

class TaskCreate(TaskBase):
    """タスク作成"""
    pass


class TaskCreateResponse(TaskCreate):
    """タスク作成用のレスポンス"""
    id: int
    
    class Config:
        # モデルのデータを辞書に変換する(IMPLICIT)
        orm_mode = True
