from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.utils.password import hash_password, verify_password
from app.utils.jwt_handler import create_token

router = APIRouter(tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/auth/register")
def register(name: str, email: str, password: str, role: str = "user", db: Session = Depends(get_db)):
    try:
        print("DEBUG START")

        existing = db.query(User).filter(User.email == email).first()
        print("CHECK USER DONE")

        if existing:
            return {"error": "Email exists"}

        hashed = hash_password(password)
        print("PASSWORD HASHED")

        user = User(name=name, email=email, password=hashed, role=role)

        db.add(user)
        db.commit()
        print("DB COMMIT DONE")

        return {"message": "success"}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}

@router.post("/auth/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        return {"error": "Invalid credentials"}

    token = create_token({
        "sub": user.email,
        "role": user.role   # 👈 IMPORTANT
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }