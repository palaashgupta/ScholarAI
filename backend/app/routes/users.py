import asyncio
import bcrypt
import os
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Response, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel, EmailStr, Field
from app.supabase_client import supabase

router = APIRouter(prefix="/users", tags=["Users"])

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email_address: EmailStr
    password: str = Field(..., min_length=6)
    retype_password: str = Field(..., min_length=6)

@router.post("/register")
async def register_user(user: UserCreate):
    # Check for existing user
    existing_username = await asyncio.to_thread(
        lambda: supabase.table("users")
        .select("*")
        .or_(f"username.eq.{user.username}")
        .execute()
    )

    existing_email = await asyncio.to_thread(
        lambda: supabase.table("users")
        .select("*")
        .or_(f"email_address.eq.{user.email_address}")
        .execute()
    )

    #Check whether username already in use
    if existing_username.data:
        raise HTTPException(status_code=400, detail="User already exists")

    #Check whether email already in use
    if existing_email.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate passwords
    if user.password != user.retype_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Hash password
    hashed_pw = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    # Insert user
    result = await asyncio.to_thread(
        lambda: supabase.table("users").insert({
            "username": user.username,
            "hash_password": hashed_pw.decode("utf-8"),
            "email_address": user.email_address,
        }).execute()
    )

    # ✅ New way to check for success
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create user")

    return {"message": "User created successfully", "user_id": result.data[0]["user_id"]}

@router.post("/login")
async def user_login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password
    result = await asyncio.to_thread(
        lambda: supabase.table("users")
        .select("*")
        .eq("email_address", email)
        .execute()
    )
    
    if not result.data:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    user = result.data[0]
    hashed_pw = user["hash_password"].encode("utf-8")

    if not bcrypt.checkpw(password.encode("utf-8"), hashed_pw):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    token = jwt.encode(
        {"user_id": user["user_id"], "exp": expire},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=JWT_EXPIRE_MINUTES * 60
    )
    return {"message": "Login successful","user_id": user["user_id"]}

@router.post("/logout")
async def user_logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"} 


def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not logged in")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired")
    
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user_id


@router.get("/me")
async def get_me(user_id: str = Depends(get_current_user)):
    """Returns the current logged-in user info."""
    result = await asyncio.to_thread(
        lambda: supabase.table("users").select("user_id,username,email_address,role").eq("user_id", user_id).execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")

    return result.data[0]