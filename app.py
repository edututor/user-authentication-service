from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from routes.auth import auth_router
from core.database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
import os

app = FastAPI()
# Include authentication routes
app.include_router(auth_router)
Base.metadata.create_all(bind=engine)
# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def create_new_user():
    return JSONResponse(
        status_code=200,
        content={"message": "Your account is created successfully!"},
    )


@app.get("/api/delete-user")
def delete_user(db: Session = Depends(get_db)):
    """Leave it for now!!"""
    return {"message": "Welcome to the Authentication API!"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
