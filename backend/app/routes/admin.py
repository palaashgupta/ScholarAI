import asyncio
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, Field
from app.supabase_client import supabase
from app.routes.users import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

### Get all Users
@router.get("/users")
async def get_all_users(request: Request, admin_id: str = Depends(get_current_user)):
    admin_user = supabase.table("users").select("*").eq("user_id", admin_id).execute().data
    if not admin_user or admin_user[0]["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    
    result = await asyncio.to_thread(
        lambda: supabase.table("users").select("user_id,username,email_address,role").execute()
    )

    
    if result.data == []:
        raise HTTPException(status_code= 404, detail = "Error in Fetching users")

    return result.data

### Get all Queries
@router.get("/queries")
async def get_all_queries(request: Request, admin_id: str = Depends(get_current_user)):
    admin_user = supabase.table("users").select("*").eq("user_id", admin_id).execute().data
    if not admin_user or admin_user[0]["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    
    result = await asyncio.to_thread(
        lambda: supabase.table("search_query").select("*").execute()
    )

    
    if result.data == []:
        raise HTTPException(status_code= 404, detail = "Error in Fetching queries")

    return result.data

### Get all Research Papers
@router.get("/research-papers")
async def get_all_research_papers(request: Request, admin_id: str = Depends(get_current_user)):
    admin_user = supabase.table("users").select("*").eq("user_id", admin_id).execute().data
    if not admin_user or admin_user[0]["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    
    result = await asyncio.to_thread(
        lambda: supabase.table("paper_information").select("*").execute()
    )

    if result.data == []:
        raise HTTPException(status_code= 404, detail = "Error in Fetching research papers")

    return result.data

### Delete user by id
@router.delete("/users/{user_id}")
async def delete_user(user_id: int, admin_id: str = Depends(get_current_user)):
    admin_user = supabase.table("users").select("*").eq("user_id", admin_id).execute().data
    if not admin_user or admin_user[0]['role'] != "ADMIN":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")

    result = await asyncio.to_thread(
        lambda: supabase.table("users").delete().eq("user_id", user_id).execute()
    )

    if result.data == []:
        raise HTTPException(status_code= 404, detail= f"User with {user_id} not found!")

    return {
        "message": f"User with {user_id} deleted successfully!"
    }


### Delete research paper by id
@router.delete("/research-paper/{paper_id}")
async def delete_paper(paper_id: int, admin_id: str = Depends(get_current_user)):
    admin_user = supabase.table("users").select("*").eq("user_id",admin_id).execute().data
    if not admin_user or admin_user[0]['role'] != "ADMIN":
        raise HTTPException(status_code = 403, detail="Access forbidden: Admin only")

    result = await asyncio.to_thread(
        lambda: supabase.table("paper_information").delete().eq("paper_id",paper_id).execute()
    )

    if result.data == []:
        raise HTTPException(status_code=404, detail=f"Paper with {paper_id} not found!")

    return {
        "message": f"Paper with {paper_id} deleted successfully!"
    }
