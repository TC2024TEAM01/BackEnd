# from fastapi import FastAPI,Depends
# from dotenv import load_dotenv
# from pydantic import BaseModel
# from sqlalchemy import create_engine,CheckConstraint, Column, Integer, String, Text, ForeignKey, Table, Date,Time, text,inspect
# from sqlalchemy.orm import declarative_base, relationship, sessionmaker,Session

# from sqlalchemy.ext.declarative import declarative_base
# import os


# from sqlalchemy.dialects import registry
# print(registry.load("postgresql.psycopg2"))
# load_dotenv()

# app = FastAPI() 

# DATABASE_URL=os.getenv("DB_URL")
# connection_string = f"{DATABASE_URL}?sslmode=verify-ca&sslrootcert="
 

# engine = create_engine( 
#     DATABASE_URL
# ) 
# try:
#     with engine.connect() as connection:
#         print("Connection successful!")
# except Exception as e:
#     print(f"Connection failed: {e}")

# Base = declarative_base()

# SessionLocal = sessionmaker(bind=engine)
# session = SessionLocal()
# try:
#     # Create a session
#     session = SessionLocal()
#     # Test a query to fetch table names
#     inspector = inspect(engine)
#     tables = inspector.get_table_names()
#     print("Connected! Tables in the database:", tables)
# except Exception as e:
#     print(f"Session creation failed: {e}")
# finally:
#     session.close()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# class Task(Base):
#     __tablename__ = 'Tasks'

#     task_id = Column(Integer, primary_key=True, server_default=text("nextval('\"Tasks_task_id_seq\"'::regclass)"))
#     title = Column(String, nullable=False)
#     desc = Column(Text)
#     status = Column(String, server_default=text("'pending'::character varying"))

#     users = relationship('User', secondary='employee_tasks')


# class User(Base):
#     __tablename__ = 'Users'

#     user_id = Column(Integer, primary_key=True, server_default=text("nextval('\"Users_id_seq\"'::regclass)"))
#     nom = Column(String, nullable=False)
#     prenom = Column(String, nullable=False)
#     email = Column(String, nullable=False)
#     pwd = Column(String, nullable=False)
#     role = Column(String, nullable=False)
#     num_tlph = Column(String, nullable=False)


# class Conge(Base):
#     __tablename__ = 'conges'
#     __table_args__ = (
#         CheckConstraint("(status)::text = ANY ((ARRAY['En attente'::character varying, 'ApprouvÚ'::character varying, 'RefusÚ'::character varying])::text[])"),
#         CheckConstraint('date_fin >= date_debut')
#     )

#     conge_id = Column(Integer, primary_key=True, server_default=text("nextval('conges_conge_id_seq'::regclass)"))
#     user_id = Column(ForeignKey('Users.user_id'), nullable=False)
#     date_debut = Column(Date, nullable=False)
#     date_fin = Column(Date, nullable=False)
#     status = Column(String(50), nullable=False, server_default=text("'pending'::character varying"))

#     user = relationship('User')


# class Dailyreport(Base):
#     __tablename__ = 'dailyreport'

#     report_id = Column(Integer, primary_key=True, server_default=text("nextval('dailyreport_report_id_seq'::regclass)"))
#     user_id = Column(ForeignKey('Users.user_id'), nullable=False)
#     report_date = Column(Date, nullable=False)
#     heure_check_in = Column(Time)
#     heure_check_out = Column(Time)
#     status = Column(String(50))
#     bonus = Column(Integer)

#     user = relationship('User')


# t_employee_tasks = Table(
#     'employee_tasks', Base.metadata,
#     Column('task_id', ForeignKey('Tasks.task_id', ondelete='CASCADE'), primary_key=True, nullable=False),
#     Column('user_id', ForeignKey('Users.user_id', ondelete='CASCADE'), primary_key=True, nullable=False)
# )


# @app.get("/")
# def get_tasks(db: Session = Depends(get_db)):
#     Users = db.query(Task).all()
#     return 'pp'
from fastapi import FastAPI
from routers import Users

app = FastAPI()


# Inclure les routes des utilisateurs
app.include_router(Users.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur mon API avec FastAPI et PostgreSQL"}
