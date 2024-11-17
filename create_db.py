from sqlalchemy import create_engine
from models.base import Base
from models.ev_charger import EVCharger
from models.pricing_schedule import PricingSchedule
from models.time_slot import TimeSlot
from models.charger_schedule_assignment import ChargerScheduleAssignment
from database import get_database_url

def create_database():
    engine = create_engine(get_database_url())
    Base.metadata.create_all(engine)
    print("Database created successfully.")

if __name__ == "__main__":
    create_database()