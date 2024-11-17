from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ChargerScheduleAssignment(Base):
    __tablename__ = 'charger_schedule_assignment'
    assignment_id = Column(Integer, primary_key=True)
    charger_id = Column(Integer, ForeignKey('ev_chargers.charger_id'))
    schedule_id = Column(Integer, ForeignKey('pricing_schedules.schedule_id'))
    effective_from = Column(Date)
    effective_to = Column(Date)
    charger = relationship("EVCharger", back_populates="assignments")
    schedule = relationship("PricingSchedule", back_populates="assignments")