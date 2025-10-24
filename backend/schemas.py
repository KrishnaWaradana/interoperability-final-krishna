from pydantic import BaseModel
from datetime import date
from typing import List, Optional

# === Participant Schemas ===
# Schema dasar untuk Participant
class ParticipantBase(BaseModel):
    name: str
    email: str

# Schema untuk membuat participant baru (termasuk event_id)
class ParticipantCreate(ParticipantBase):
    event_id: int

# Schema untuk membaca data participant (termasuk id)
class Participant(ParticipantBase):
    id: int
    event_id: int

    class Config:
        orm_mode = True  # Mengizinkan Pydantic membaca dari model SQLAlchemy

# === Event Schemas ===
# Schema dasar untuk Event
class EventBase(BaseModel):
    title: str
    date: date
    location: str
    quota: int

# Schema untuk membuat event baru
class EventCreate(EventBase):
    pass

# Schema untuk membaca data event, termasuk daftar pesertanya
class Event(EventBase):
    id: int
    participants: List[Participant] = []  # Akan berisi daftar peserta

    class Config:
        orm_mode = True