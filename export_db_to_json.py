# python export_db_to_json.py


import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,  declarative_base, relationship
from db.models import *  # Import your database models
from core.config import settings
engine = create_engine(settings.DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

data = session.query(Base).all()

json_data = [item.to_dict() for item in data]

with open("exported_data.json", "w") as f:
    json.dump(json_data, f, indent=4)

session.close()
print("Database export completed successfully.")