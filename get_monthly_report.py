from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, and_
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import date, timedelta

app = FastAPI()
engine = create_engine("your_database_connection_string")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    attendance = relationship("Attendance", back_populates="employee")


class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    status = Column(String)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    employee = relationship("Employee", back_populates="attendance")


@app.get("/report/{year}/{month}")
def generate_monthly_report(year: int, month: int):
    db = SessionLocal()

    start_date = date(year, month, 1)
    end_date = start_date.replace(day=28) + timedelta(days=4)
    if end_date.day > 28:
        end_date = end_date.replace(day=28)

    employees = (
        db.query(Employee)
        .outerjoin(Attendance, and_(Attendance.employee_id == Employee.id, Attendance.date >= start_date, Attendance.date <= end_date))
        .all()
    )

    report_data = []
    current_date = start_date
    while current_date <= end_date:
        report_data.append({
            "date": current_date.isoformat(),
            "employees": [
                {
                    "employee_id": employee.id,
                    "name": employee.name,
                    "attendance_status": get_attendance_status(employee, current_date)
                }
                for employee in employees
            ]
        })
        current_date += timedelta(days=1)

    db.close()

    return report_data


def get_attendance_status(employee, current_date):
    attendance = next((attendance for attendance in employee.attendance if attendance.date == current_date), None)
    return attendance.status if attendance else "Not available"
