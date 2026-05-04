from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE CONNECTION
engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False}
)

# SESSION
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# BASE MODEL
Base = declarative_base()

# ✅ VERY IMPORTANT (THIS WAS MISSING)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()