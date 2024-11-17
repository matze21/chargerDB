from database import get_database_url
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.time_slot import TimeSlot

def add_bulk_samples():
    engine = create_engine(get_database_url())
    session = Session(engine)

    # define pricing updates e.g. 
    # we'd neeed to know which schedules from which stations we need to udpate
    # potentially we also need to create new ones
    pricing_updates=[
        {'id': 1, 'price_per_kwh': 0.15},
        {'id': 2, 'price_per_kwh': 0.20},
        {'id': 3, 'price_per_kwh': 0.25}]

    session.bulk_update_mappings(TimeSlot, pricing_updates)
    session.commit()

def __main__():
    add_bulk_samples()