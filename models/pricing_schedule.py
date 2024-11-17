from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from .base import Base

class PricingSchedule(Base):
    __tablename__ = 'pricing_schedules'

    schedule_id = Column(Integer, primary_key=True)
    schedule_name = Column(String(100), nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=False)

    time_slots = relationship("TimeSlot", back_populates="schedule")
    assignments = relationship("ChargerScheduleAssignment", back_populates="schedule")