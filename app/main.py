from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import datetime

tasks = {}         # key = task id (int), value = task dict
task_counter = 0   # auto-incrementing ID
creation_log = []  # stores the date each task was created


app = FastAPI(title="To-Do List API")

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


@app.get("/")
def root():
    return {"message": "To-Do List API is running!"}

@app.get("/tasks")
def get_all_tasks():
    return {"tasks": list(tasks.values()), "total": len(tasks)}

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    global task_counter
    task_counter += 1
    now = datetime.datetime.now().isoformat()
    new_task = {
        "id": task_counter,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": now,
    }
    tasks[task_counter] = new_task
    creation_log.append(now[:10])  # store YYYY-MM-DD only
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    stored = tasks[task_id]
    if task.title is not None:
        stored["title"] = task.title
    if task.description is not None:
        stored["description"] = task.description
    if task.completed is not None:
        stored["completed"] = task.completed
    return stored

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    deleted = tasks.pop(task_id)
    return {"message": f"Task '{deleted['title']}' deleted"}

@app.get("/stats")
def get_stats():
    total = len(tasks)
    completed = sum(1 for t in tasks.values() if t["completed"])
    pending = total - completed
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "creation_log": creation_log,
    }





if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
