from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

@router.get("/users")
def get_users():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM public."Users" ORDER BY user_id ASC')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Transformer les données en dictionnaires
        users = [
            {
                "user_id": row[0],
                "nom": row[1],
                "prenom": row[2],
                "email": row[3],
                "pwd": row[4],
                "role": row[5],
                "num_tlph": row[6],
            }
            for row in rows
        ]
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/users")
def create_user(
    nom: str,
    prenom: str,
    email: str,
    pwd: str,
    role: str,
    num_tlph: str
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Insertion dans la table
        cursor.execute(
            'INSERT INTO public."Users" (nom, prenom, email, pwd, role, num_tlph) VALUES (%s, %s, %s, %s, %s, %s) RETURNING user_id',
            (nom, prenom, email, pwd, role, num_tlph)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        return {"user_id": user_id, "message": "Utilisateur créé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

