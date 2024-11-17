from sqlalchemy import Column, Integer, String, Numeric, Time, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class TimeSlot(Base):
    __tablename__ = 'time_slots'
    slot_id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey('pricing_schedules.schedule_id'))
    start_time = Column(Time)
    end_time = Column(Time)
    price_per_kwh = Column(Numeric(10, 2))
    schedule = relationship("PricingSchedule", back_populates="time_slots")