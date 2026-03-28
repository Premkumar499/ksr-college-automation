import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from sqlalchemy import create_engine, inspect
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
inspector = inspect(engine)

for table_name in inspector.get_table_names():
    print(f"\nTable: {table_name}")
    for column in inspector.get_columns(table_name):
        print(f"  - {column['name']} ({column['type']})")
