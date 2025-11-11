import asyncio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from supabase_client import supabase
import bcrypt

router = APIRouter(prefix="/users", tags=["Users"])

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
