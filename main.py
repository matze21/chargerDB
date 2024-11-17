import configparser
from sqlalchemy import create_engine

config = configparser.ConfigParser()
config.read('config.ini')

db_config = config['database']
engine = create_engine(f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

from database import init_db, get_session
from models import EVCharger, PricingSchedule, TimeSlot, ChargerScheduleAssignment, CurrentChargerPricing

def main():
    init_db()
    session = get_session()

    # Your main logic here
    # For example:
    charger = EVCharger(location='Test Location', time_zone='UTC')
    session.add(charger)
    session.commit()

if __name__ == "__main__":
    main()