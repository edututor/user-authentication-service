from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """Schema for user signup request"""
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema for returning user data (excluding password)"""
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    """Schema for user login request"""
    email: EmailStr
    password: str

class UserDelete(BaseModel):
    """Schema for user deletion request"""
    email: EmailStr

class TokenResponse(BaseModel):
    """Schema for returning JWT token after login"""
    access_token: str
    token_type: str = "bearer"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse  # Include user info

