from fastapi import FastAPI , HTTPException
from pydantic import BaseModel , Field
from datetime import datetime
from typing import Optional
from typing import ClassVar
from enum import Enum

app = FastAPI()


class IDGenerator:
    counter: ClassVar[int] = 1

    @classmethod
    def get_id(cls) -> int:
        id_ = cls.counter
        cls.counter += 1
        return id_


class TaskStatus(str , Enum):
    in_progress = "in Progress"
    pending = "Pending"
    finished = "Fnished"
    completed = "Completed"

class Task(BaseModel):
    id: int =  Field(default_factory=IDGenerator.get_id)
    name : str
    description : str
    status: TaskStatus = TaskStatus.pending  
    created_at: datetime = Field(default_factory=datetime.utcnow) 
    completed_at: Optional[datetime] = None
    execution_duration: Optional[float] = None
    

tasks_db = [
    Task(
        id=1,
        name="yahia",
        description="string",
        status=TaskStatus.pending,
        created_at=datetime(2025, 7, 26, 14, 32, 56, 43485),
        completed_at=datetime(2025, 7, 26, 11, 53, 7, 292000),
        execution_duration=0.0
    )
]




@app.get('/')
def index():
    return {'message' : 'Hello, To Task Scheduler!'}

@app.post('/create-tasks') # status , time of end, execution duration 
def create_tasks(task : Task):
    tasks_db.append(task)
    return{ 
        "message": "Task created successfully",
        "task_id": str(task.id),
        "status": task.status,
        "created_at": task.created_at
        }

@app.get('/tasks') # pagination , priority filtering , sorting by creation time
def show_tasks():
    return tasks_db

@app.get('/tasks/{task_id}', response_model = Task)
def show_task_description(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete('/delete_tasks/{task_id}')
def delete_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            tasks_db.remove(task)
            return {"message": f"Task with ID {task_id} deleted successfully."}
    raise HTTPException(status_code=404, detail="Task not found")

    

@app.get('/tasks/history') # search by desciption or parameters
def show_history():
    pass





