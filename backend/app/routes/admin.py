from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, Field
from app.supabase_client import supabase
from app.routes.users import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

### Get all Users

### Get all Queries

### Get all Research Papers


### Delete user by id

### Delete query by id

### Delete research paper by id