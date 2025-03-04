from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.schemas import UserCreate, UserResponse, TokenResponse, UserLogin
from models.user import User
from core.database import SessionLocal
from core.security import hash_password, verify_password, create_access_token

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# Dependency: Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Handles user signup and stores data in the database"""

    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash the password
        hashed_password = hash_password(user_data.password)

        # Create new user object
        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            hashed_password=hashed_password
        )

        # Save to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user  # FastAPI will return only id, name, and email (schema-defined)

    except Exception as e:
        return HTTPException(status_code=400, detail=f"An error occured while attempting to create a new user: {e}")


@auth_router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Handles user login and returns JWT token"""

    # Find user by email
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Verify password
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT token
    access_token = create_access_token({"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}

