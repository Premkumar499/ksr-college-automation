import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app.core.database import SessionLocal
from app.models.database import Scholarship

db = SessionLocal()
count = db.query(Scholarship).count()
print(f"Total scholarships in DB: {count}")
for s in db.query(Scholarship).all():
    print(f"- {s.name} (Active: {s.is_active})")
