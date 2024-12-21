
from fastapi import FastAPI
from routers import Users
from routers import Conges
from routers import DailyReports
from routers import tasks

app = FastAPI()

 
# Inclure les routes des utilisateurs
#app.include_router(Users.router)
#app.include_router(Conges.router)
#app.include_router(DailyReports.router)

# Inclure les routes des tâches
#app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur mon API avec FastAPI et PostgreSQL"}
 