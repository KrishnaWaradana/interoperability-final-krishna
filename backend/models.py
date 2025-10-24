from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100))
    date = Column(Date)
    location = Column(String(100))
    quota = Column(Integer)

    # Relasi: Satu event punya banyak participant
    participants = relationship("Participant", back_populates="event")

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100))
    event_id = Column(Integer, ForeignKey("events.id"))

    # Relasi: Participant ini terdaftar di satu event
    event = relationship("Event", back_populates="participants")