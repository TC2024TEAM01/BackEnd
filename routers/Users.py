from fastapi import APIRouter, HTTPException
from database import get_connection
from pydantic import BaseModel
router = APIRouter()
class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: str
    pwd: str
    role: str
    num_tlph: str
class UserUpdate(BaseModel):
    nom: str|None=None
    prenom:str|None=None 
    email: str|None=None
    pwd: str|None=None
    role: str|None=None
    num_tlph: str|None=None

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


 # Get user by name
@router.get("users/userByName")
def get_user_by_name(name: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM public."Users" WHERE nom ILIKE %s', (f"%{name}%",))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

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
   user:UserCreate
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Insertion dans la table
        cursor.execute(
            'INSERT INTO public."Users" (nom, prenom, email, pwd, role, num_tlph) VALUES (%s, %s, %s, %s, %s, %s) RETURNING user_id',
            (user.nom, user.prenom, user.email, user.pwd, user.role, user.num_tlph)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        return {"user_id": user_id, "message": "Utilisateur créé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update user
@router.patch("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Build dynamic query
        update_fields = []
        values = []

        for key, value in user.dict(exclude_unset=True).items():
            update_fields.append(f"{key} = %s")
            values.append(value)

        values.append(user_id)

        query = f'UPDATE public."Users" SET {", ".join(update_fields)} WHERE user_id = %s'
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Utilisateur mis à jour avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Delete user
@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM public."Users" WHERE user_id = %s', (user_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Utilisateur supprimé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
    
# Get employees
@router.get("/users/employees")
def get_employees():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM public."Users" WHERE role = %s', ('Employee',))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        employees = [
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
        return {"employees": employees}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get user by ID
@router.get("/users/{user_id}")
def get_user(user_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM public."Users" WHERE user_id = %s', (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return {
                "user_id": row[0],
                "nom": row[1],
                "prenom": row[2],
                "email": row[3],
                "pwd": row[4],
                "role": row[5],
                "num_tlph": row[6],
            }
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 