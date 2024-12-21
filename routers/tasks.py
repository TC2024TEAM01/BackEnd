

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User, Task, EmployeeTask
from pydantic import BaseModel
from database import get_connection
from datetime import date
from typing import List
from typing import Optional
# Initialisation du routeur
router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: str
    delay: date
    user_ids: list[int]

@router.post("/tasks")
def create_task(task: TaskCreate):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO public.tasks (title, description, status, delay) VALUES (%s, %s, %s, %s) RETURNING task_id',
            (task.title, task.description, 'pending', task.delay)
        )
        task_id = cursor.fetchone()[0]

        # Assign users to the task
        for user_id in task.user_ids:
            cursor.execute(
                'INSERT INTO public.employee_tasks (task_id, user_id) VALUES (%s, %s)',
                (task_id, user_id)
            )

        conn.commit()
        cursor.close()
        conn.close()

        return {"task_id": task_id, "message": "Task created and assigned to employees successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class Task(BaseModel):
    task_id: int
    title: str
    description: str
    status: str
    delay: date

@router.get("/tasks/{user_id}")
def get_tasks_by_employee(user_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT tasks.task_id, tasks.title, tasks.description, tasks.status, tasks.delay '
            'FROM public.tasks '
            'JOIN public.employee_tasks ON tasks.task_id = employee_tasks.task_id '
            'WHERE employee_tasks.user_id = %s',
            (user_id,)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        tasks = [
            {
                "task_id": row[0],
                "title": row[1],
                "description": row[2],
                "status": row[3],
                "delay": row[4],
            }
            for row in rows
        ]
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    delay: Optional[date] = None
    status: Optional[str] = None

@router.patch("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Mise à jour conditionnelle des champs
        update_fields = []
        update_values = []
        
        if task_update.title:
            update_fields.append("title = %s")
            update_values.append(task_update.title)
        if task_update.description:
            update_fields.append("description = %s")
            update_values.append(task_update.description)
        if task_update.delay:
            update_fields.append("delay = %s")
            update_values.append(task_update.delay)
        if task_update.status:
            update_fields.append("status = %s")
            update_values.append(task_update.status)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields provided to update")

        # Ajouter l'ID de la tâche pour finaliser la requête
        update_values.append(task_id)
        
        # Construire la requête d'update
        cursor.execute(
            f'UPDATE public.tasks SET {", ".join(update_fields)} WHERE task_id = %s',
            tuple(update_values)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": f"Task {task_id} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM public.tasks WHERE task_id = %s', (task_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": f"Task {task_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
class TaskUpdateStatus(BaseModel):
    status: Optional[str]

@router.patch("/tasks/{task_id}/status")
def update_task_status(task_id: int, status_update: TaskUpdateStatus):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Mise à jour du statut de la tâche
        cursor.execute(
            'UPDATE public.tasks SET status = %s WHERE task_id = %s',
            (status_update.status, task_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": f"Task {task_id} status updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    