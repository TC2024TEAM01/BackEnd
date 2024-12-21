from fastapi import APIRouter, HTTPException
from database import get_connection
from pydantic import BaseModel
router = APIRouter()

class CongeCreate(BaseModel):
    user_id: int
    date_debut: str
    date_fin: str

class CongeUpdateStatus(BaseModel):
    status: str


@router.post("/conges")
def create_conge(conge: CongeCreate):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO public.conges (user_id, date_debut, date_fin, status) VALUES (%s, %s, %s, %s) RETURNING conge_id',
            (conge.user_id, conge.date_debut, conge.date_fin, 'pending')
        )
        conge_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        return {"conge_id": conge_id, "message": "Conge créé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
      
@router.get("/conges")
def get_conges():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM public.conges ORDER BY conge_id ASC')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        conges = [
            {
                "conge_id": row[0],
                "user_id": row[1],
                "date_debut": row[2],
                "date_fin": row[3],
                "status": row[4],
            }
            for row in rows
        ]
        return {"conges": conges}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
      
@router.patch("/conges/{conge_id}")
def update_conge_status(conge_id: int, conge_update: CongeUpdateStatus):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE public.conges SET status = %s WHERE conge_id = %s',
            (conge_update.status, conge_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Statut du conge mis à jour avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
