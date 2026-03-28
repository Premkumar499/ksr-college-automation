import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
with engine.connect() as conn:
    res = conn.execute(text("SELECT COUNT(*) FROM scholarships"))
    print("COUNT:", res.scalar())
