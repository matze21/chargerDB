from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models.ev_charger import EVCharger
from models.pricing_schedule import PricingSchedule
from models.time_slot import TimeSlot
from models.charger_schedule_assignment import ChargerScheduleAssignment
from database import get_database_url
from datetime import date, time

def add_sample_data():
    engine = create_engine(get_database_url())
    session = Session(engine)

    try:
        # Create sample EV Chargers
        charger1 = EVCharger(location="Downtown Station", details="Fast Charging Available")
        charger2 = EVCharger(location="Shopping Mall", details="4 Charging Points")
        session.add_all([charger1, charger2])

        # Create sample Pricing Schedules
        schedule1 = PricingSchedule(
            schedule_name="Standard Weekday",
            effective_from=date(2024, 1, 1),
            effective_to=date(2024, 12, 31)
        )
        schedule2 = PricingSchedule(
            schedule_name="Weekend Special",
            effective_from=date(2024, 1, 1),
            effective_to=date(2024, 12, 31)
        )
        session.add_all([schedule1, schedule2])

        # Create sample Time Slots
        time_slots = [
            TimeSlot(schedule=schedule1, start_time=time(0, 0), end_time=time(6, 0), price_per_kwh=0.10),
            TimeSlot(schedule=schedule1, start_time=time(6, 0), end_time=time(18, 0), price_per_kwh=0.25),
            TimeSlot(schedule=schedule1, start_time=time(18, 0), end_time=time(23, 59), price_per_kwh=0.15),
            TimeSlot(schedule=schedule2, start_time=time(0, 0), end_time=time(12, 0), price_per_kwh=0.12),
            TimeSlot(schedule=schedule2, start_time=time(12, 0), end_time=time(23, 59), price_per_kwh=0.18)
        ]
        session.add_all(time_slots)

        # Create sample Charger Schedule Assignments
        assignment1 = ChargerScheduleAssignment(
            charger=charger1,
            schedule=schedule1,
            effective_from=date(2024, 1, 1),
            effective_to=date(2024, 12, 31)
        )
        assignment2 = ChargerScheduleAssignment(
            charger=charger2,
            schedule=schedule2,
            effective_from=date(2024, 1, 1),
            effective_to=date(2024, 12, 31)
        )
        session.add_all([assignment1, assignment2])

        session.commit()
        print("Sample data added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    add_sample_data()