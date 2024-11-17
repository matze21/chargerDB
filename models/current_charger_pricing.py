from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class CurrentChargerPricing(Base):
    __tablename__ = 'current_charger_pricing'
    charger_id = Column(Integer, ForeignKey('ev_chargers.charger_id'), primary_key=True)
    current_price = Column(Numeric(10, 2))
    price_effective_from = Column(DateTime)
    price_effective_to = Column(DateTime)
    last_updated = Column(DateTime)
    charger = relationship("EVCharger", back_populates="current_pricing")