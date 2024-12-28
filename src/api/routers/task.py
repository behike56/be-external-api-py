from fastapi import APIRouter

import api.schemas.task as task_schema

router = APIRouter()

@router.get("/tasks", response_model=list[task_schema.Task])
async def list_tsks():
    return [task_schema.Task(id=1, title="first task")]

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_tsks(task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=1, **task_body.dict())
    

@router.put("/tasks/{task_id}")
async def update_task():
    pass

@router.delete("/tasks/{task_id}")
async def delete_task():
    pass