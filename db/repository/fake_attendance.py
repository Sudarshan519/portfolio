from datetime import date,datetime,timedelta
import random

from faker import Faker
from db.models.attendance import AttendanceModel, EmployeeModel
ph_no = []
  
# the first number should be in the range of 6 to 9
ph_no.append(random.randint(6, 9))
start_date = date.today() - timedelta(days=40)  # Start date for the date range
end_date = date.today()-timedelta(days=0)  # End date for the date range
fake = Faker()
class FakeAttendance:
    @staticmethod
    def addEmployee(db):
        try:
            fake = Faker()
            employees = []
            for _ in range(100):
                employee = EmployeeModel(
                    name=fake.name(),
                    # email=fake.email(),
                    phone= (random.randint(9800000000, 9900000000))
                )
                employees.append(employee)

            # Write employees to the database
            db.bulk_save_objects(employees)

            # Commit the changes to the database
            db.commit()
            return employees
        except Exception as e:
            return e

    @staticmethod
    def addAttendance(db):
        attendance_records=[]
        employees=db.query(EmployeeModel).all()
        try:
            for _ in range(10):
                random_employee = random.choice(employees)
                random_date = fake.date_between_dates(date_start=start_date, date_end=end_date)

                attendance_record = AttendanceModel(
                    employee_id=random_employee.id,
                    attendance_date=random_date,
                    login_time='10:00',
                    logout_time='10:50'

                )
                attendance_records.append(attendance_record)
                db.add(attendance_record)
                db.commit()
        except Exception as e:
            return None
        # Write attendance records to the database
        db.bulk_save_objects(attendance_records)
        db.commit()
        return attendance_record