from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class EVCharger(Base):
    __tablename__ = 'ev_chargers'
    charger_id = Column(Integer, primary_key=True)
    location = Column(String(255))
    time_zone = Column(String(50))
    details = Column(String(255))
    assignments = relationship("ChargerScheduleAssignment", back_populates="charger")
    #current_pricing = relationship("CurrentChargerPricing", uselist=False, back_populates="charger")