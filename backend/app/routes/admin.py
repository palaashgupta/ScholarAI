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
        lambda: supabase.table("users").select("user_id,created_at,username,email_address,role").order("created_at", desc=True).execute()
    )

    
    if result.data == []:
        raise HTTPException(status_code= 404, detail = "Error in Fetching users")

    return result.data

### Get all Queries
# Get all search queries (deduplicated by user_id + query_text)
@router.get("/queries")
async def get_all_queries(admin_id: str = Depends(get_current_user)):
    # Check admin role
    admin_user = supabase.table("users").select("*").eq("user_id", admin_id).execute().data
    if not admin_user or admin_user[0]["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    
    result = await asyncio.to_thread(
        lambda: supabase.table("search_query").select("*").order("created_at", desc=True).execute()
    )
    
    if result.data is None:
        return []

    # Deduplicate queries by user_id + query_text
    seen = set()
    deduped_queries = []
    for q in result.data:
        key = (q["user_id"], q["query"])
        if key not in seen:
            deduped_queries.append(q)
            seen.add(key)

    return deduped_queries

# Delete queries by user_id + query_text (all matching records)
@router.delete("/queries")
async def delete_queries(user_id: int, query_text: str, admin_id: str = Depends(get_current_user)):
    # Check admin role
    admin_user = supabase.table("users").select("*").eq("user_id", admin_id).execute().data
    if not admin_user or admin_user[0]["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")

    # Delete all matching queries
    result = await asyncio.to_thread(
        lambda: supabase.table("search_query")
        .delete()
        .eq("user_id", user_id)
        .eq("query", query_text)
        .execute()
    )

    return {"message": f"All queries for user_id={user_id} with query='{query_text}' deleted successfully."}

### Get all Research Papers
@router.get("/research-papers")
async def get_all_research_papers(request: Request, admin_id: str = Depends(get_current_user)):
    admin_user = supabase.table("users").select("*").eq("user_id", admin_id).execute().data
    if not admin_user or admin_user[0]["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    
    result = await asyncio.to_thread(
        lambda: supabase.table("paper_information").select("*").order("created_at", desc=True).execute()
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

@router.delete("/queries/{query_id}")
async def delete_query(query_id: int, admin_id: str = Depends(get_current_user)):
    admin_user = supabase.table("users").select("*").eq("user_id", admin_id).execute().data
    if not admin_user or admin_user[0]['role'] != "ADMIN":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")

    result = await asyncio.to_thread(
        lambda: supabase.table("search_query").delete().eq("query_id", query_id).execute()
    )

    if result.data == []:
        raise HTTPException(status_code= 404, detail= f"User with {user_id} not found!")

    return {
        "message": f"Query with {query_id} deleted successfully!"
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

@router.get("/stats")
async def get_admin_stats(admin_id: str = Depends(get_current_user)):
    # Check admin role
    admin_user = supabase.table("users").select("*").eq("user_id", admin_id).execute().data
    if not admin_user or admin_user[0]['role'] != "ADMIN":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    
    # Total users
    total_users_res = await asyncio.to_thread(lambda: supabase.table("users").select("*").execute())
    total_users = len(total_users_res.data) if total_users_res.data else 0

    # Total queries
    total_queries_res = await asyncio.to_thread(lambda: supabase.table("search_query").select("*").execute())
    total_queries = len(total_queries_res.data) if total_queries_res.data else 0

    # Queries by guests (user_id = 0)
    guest_queries = len([q for q in total_queries_res.data if q["user_id"] == 0]) if total_queries_res.data else 0

    # Total research papers
    total_papers_res = await asyncio.to_thread(lambda: supabase.table("paper_information").select("*").execute())
    total_papers = len(total_papers_res.data) if total_papers_res.data else 0

    return {
        "total_users": total_users,
        "total_queries": total_queries,
        "guest_queries": guest_queries,
        "total_papers": total_papers
    }
