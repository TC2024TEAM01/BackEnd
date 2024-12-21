from fastapi import APIRouter, HTTPException
from database import get_connection
from pydantic import BaseModel

router = APIRouter()

class ReportCreate(BaseModel):
    user_id: int
    report_date: str
class CongeUpdateStatus(BaseModel):
    status: str
@router.get("/reportsById")
def get_reports_by_id(user_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM public.dailyreport WHERE user_id = %s', (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        reports = [
            {
                "report_id": row[0],
                "user_id": row[1],
                "report_date": row[2],
                "heure_check_in": row[3],
                "heure_check_out": row[4],
                "status": row[5],
                "bonus": row[6]
            } for row in rows
        ]
        return {"reports": reports}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/reportsByDay")
def get_reports_by_day(day: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM public.dailyreport WHERE report_date = %s', (day,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        reports = [
            {
                "report_id": row[0],
                "user_id": row[1],
                "report_date": row[2],
                "heure_check_in": row[3],
                "heure_check_out": row[4],
                "status": row[5],
                "bonus": row[6]
            } for row in rows
        ]
        return {"reports": reports}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get report by day and name
@router.get("/reports")
def get_report(day: str, user_id: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM public.dailyreport WHERE report_date = %s AND user_id = %s', (day, user_id))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        reports = [
            {
                "report_id": row[0],
                "user_id": row[1],
                "report_date": row[2],
                "heure_check_in": row[3],
                "heure_check_out": row[4],
                "status": row[5],
                "bonus": row[6]
            } for row in rows
        ]
        return {"reports": reports}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Scheduler to mark absent reports at 5 PM and create reports at 12 AM
import schedule
import time
from datetime import datetime, timedelta

def mark_absent():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE public.dailyreport SET status = 'abscent' WHERE heure_check_in IS NULL AND report_date = CURRENT_DATE")
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error marking absent: {str(e)}")

def create_daily_reports():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO public.dailyreport (user_id, report_date, status) SELECT user_id, CURRENT_DATE, 'pending' FROM public.\"Users\"")
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating daily reports: {str(e)}")

schedule.every().day.at("17:00").do(mark_absent)
schedule.every().day.at("00:00").do(create_daily_reports)

while True:
    schedule.run_pending()
    time.sleep(1)
