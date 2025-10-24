from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Tentukan URL database SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./backend/campus_events.db"

# Buat 'engine' SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Buat 'SessionLocal' class untuk sesi database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Buat 'Base' class untuk model-model kita
Base = declarative_base()