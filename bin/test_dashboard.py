import sys
import os

from app.core.database import SessionLocal
from app.services.dashboard_service import DashboardService

def test_dashboard():
    db = SessionLocal()
    try:
        service = DashboardService(db)
        data = service.get_dashboard_data()
        print(data.model_dump_json(indent=2))
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_dashboard()
