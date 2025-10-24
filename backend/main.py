from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine

# Membuat tabel di database (jika belum ada)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Campus Event Registration Platform",
    description="API untuk mengelola event kampus dan pendaftaran peserta."
)

# PENTING: Middleware untuk CORS (Cross-Origin Resource Sharing)
# Ini agar frontend (HTML) bisa mengakses API ini dari domain/port yang berbeda.
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua origin (untuk development)
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua method (GET, POST, etc.)
    allow_headers=["*"],  # Mengizinkan semua header
)


# Dependency untuk mendapatkan sesi database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === Endpoint untuk Event (Tugas 2) ===

@app.post("/events/", response_model=schemas.Event, tags=["Events"])
def create_new_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """Menambah event baru """
    return crud.create_event(db=db, event=event)


@app.get("/events/", response_model=List[schemas.Event], tags=["Events"])
def read_all_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Menampilkan semua event """
    events = crud.get_events(db, skip=skip, limit=limit)
    return events


@app.put("/events/{event_id}", response_model=schemas.Event, tags=["Events"])
def update_existing_event(event_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)):
    """Mengubah data event berdasarkan ID """
    db_event = crud.update_event(db, event_id=event_id, event=event)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@app.delete("/events/{event_id}", response_model=schemas.Event, tags=["Events"])
def delete_existing_event(event_id: int, db: Session = Depends(get_db)):
    """Menghapus event berdasarkan ID """
    db_event = crud.delete_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


# === Endpoint untuk Participant (Tugas 3) ===

@app.post("/register/", response_model=schemas.Participant, tags=["Participants"])
def register_for_event(participant: schemas.ParticipantCreate, db: Session = Depends(get_db)):
    """Mendaftarkan peserta baru ke sebuah event """
    result = crud.create_participant(db=db, participant=participant)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    if result is None:
        raise HTTPException(status_code=404, detail="Event not found")
        
    return result


@app.get("/participants/", response_model=List[schemas.Participant], tags=["Participants"])
def read_all_participants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Menampilkan semua peserta yang terdaftar """
    participants = crud.get_participants(db, skip=skip, limit=limit)
    return participants