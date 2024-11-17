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
        charger1 = EVCharger(location="SD", details="Fast Charging Available")
        charger2 = EVCharger(location="LA", details="4 Charging Points")
        charger3 = EVCharger(location="SF", details="5 Charging Points")
        charger4 = EVCharger(location="SB_DT", details="6 Charging Points")
        charger5 = EVCharger(location="SB_BE", details="7 Charging Points")
        session.add_all([charger1, charger2,charger3,charger4, charger5])

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
        schedule3 = PricingSchedule(
            schedule_name="Weekend Special 2",
            effective_from=date(2024, 1, 1),
            effective_to=date(2024, 12, 31)
        )
        schedule4 = PricingSchedule(
            schedule_name="Weekday high season",
            effective_from=date(2024, 1, 1),
            effective_to=date(2024, 12, 31)
        )
        session.add_all([schedule1, schedule2, schedule3, schedule4])

        # Create sample Time Slots
        time_slots = [
            TimeSlot(schedule=schedule1, start_time=time(0, 0), end_time=time(6, 0), price_per_kwh=0.10),
            TimeSlot(schedule=schedule1, start_time=time(6, 0), end_time=time(18, 0), price_per_kwh=0.25),
            TimeSlot(schedule=schedule1, start_time=time(18, 0), end_time=time(23, 59), price_per_kwh=0.15),
            TimeSlot(schedule=schedule2, start_time=time(0, 0), end_time=time(12, 0), price_per_kwh=0.12),
            TimeSlot(schedule=schedule2, start_time=time(12, 0), end_time=time(23, 59), price_per_kwh=0.18),
            TimeSlot(schedule=schedule3, start_time=time(0, 0), end_time=time(6, 0), price_per_kwh=0.10),
            TimeSlot(schedule=schedule3, start_time=time(6, 0), end_time=time(12, 0), price_per_kwh=0.15),
            TimeSlot(schedule=schedule3, start_time=time(12, 0), end_time=time(14, 0), price_per_kwh=0.20),
            TimeSlot(schedule=schedule3, start_time=time(14, 0), end_time=time(18, 0), price_per_kwh=0.25),
            TimeSlot(schedule=schedule3, start_time=time(18, 0), end_time=time(20, 0), price_per_kwh=0.30),
            TimeSlot(schedule=schedule3, start_time=time(20, 0), end_time=time(22, 0), price_per_kwh=0.25),
            TimeSlot(schedule=schedule3, start_time=time(22, 0), end_time=time(23, 59), price_per_kwh=0.20)
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
        assignment3 = ChargerScheduleAssignment(
            charger=charger3,
            schedule=schedule2,
            effective_from=date(2024, 1, 1),
            effective_to=date(2024, 12, 31)
        )
        assignment4 = ChargerScheduleAssignment(
            charger=charger4,
            schedule=schedule3,
            effective_from=date(2024, 1, 1),
            effective_to=date(2024, 12, 31)
        )
        assignment5 = ChargerScheduleAssignment(
            charger=charger5,
            schedule=schedule3,
            effective_from=date(2024, 1, 1),
            effective_to=date(2024, 12, 31)
        )
        session.add_all([assignment1, assignment2, assignment3, assignment4, assignment5])

        session.commit()
        print("Sample data added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    add_sample_data()