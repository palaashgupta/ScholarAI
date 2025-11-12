import asyncio
from typing import List
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, Field
from app.supabase_client import supabase
from app.routes.users import get_current_user
from app.routes.paper_information import store_paper, get_papers_by_urls
import httpx
from datetime import datetime

router = APIRouter(prefix="/search", tags=["Search"])

# ---------------------
# Request Model
# ---------------------
class SearchRequest(BaseModel):
    query: str = Field(example="Machine Learning")


# ---------------------
# Helper: Fetch papers from Semantic Scholar
# ---------------------
async def fetch_papers(query: str, limit: int = 10) -> List[dict]:
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,abstract,url,authors,venue,publicationDate"
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Error fetching papers")
        data = resp.json()

    papers = []
    for paper in data.get("data", []):
        pub_date = datetime.utcnow().date()
        if paper.get("publicationDate"):
            try:
                pub_date = datetime.fromisoformat(paper["publicationDate"]).date()
            except ValueError:
                pass

        papers.append({
            "title": paper.get("title"),
            "summary": paper.get("abstract"),
            "paper_url": paper.get("url"),
            "authors": [a["name"] for a in paper.get("authors", [])],
            "published_in": [paper.get("venue")] if paper.get("venue") else [],
            "created_at": pub_date
        })
    return papers


# ---------------------
# POST /search - Create new query
# ---------------------
@router.post("/")
async def search_papers(request_data: SearchRequest, request: Request):
    """
    Perform a search, store query, store paper info, return query with full papers
    """
    # Get user ID or assign guest
    try:
        user_id = get_current_user(request)
        if user_id is None:
            user_id = 0
    except Exception:
        user_id = 0

    # Fetch papers
    try:
        papers = await fetch_papers(request_data.query)
        paper_urls = [p["paper_url"] for p in papers if p.get("paper_url")]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch papers: {str(e)}")

    # Store query
    try:
        query_result = await asyncio.to_thread(
            lambda: supabase.table("search_query").insert({
                "user_id": user_id,
                "query": request_data.query,
                "paper_url": paper_urls
            }).execute()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save search query: {str(e)}")

    if not query_result.data:
        raise HTTPException(status_code=500, detail="Failed to save search query")

    query_id = query_result.data[0]["query_id"]

    # Store papers in paper_information
    stored_papers = []
    for paper in papers:
        paper_data = await store_paper(paper)
        if paper_data:
            stored_papers.append(paper_data)

    # Return full info for query
    return {
        "query_id": query_id,
        "user_id": user_id,
        "query": request_data.query,
        "papers": stored_papers
    }


# ---------------------
# GET /search/{query_id} - Retrieve papers for a query
# ---------------------
@router.get("/query/{query_id}")
async def get_query(query_id: int):
    """
    Return all papers for a given search query (query_id)
    """
    # Get query
    query_result = await asyncio.to_thread(
        lambda: supabase.table("search_query")
        .select("query, paper_url, user_id, created_at")
        .eq("query_id", query_id)
        .execute()
    )

    if not query_result.data:
        raise HTTPException(status_code=404, detail="Query not found")

    query_data = query_result.data[0]
    paper_urls = query_data["paper_url"]

    # Get detailed papers
    papers = await get_papers_by_urls(paper_urls)

    return {
        "query_id": query_id,
        "query": query_data["query"],
        "user_id": query_data["user_id"],
        "created_at": query_data["created_at"],
        "papers": papers
    }


# ---------------------
# GET /search/history - All queries by logged-in user
# ---------------------
@router.get("/history")
async def get_user_queries(user_id: int = Depends(get_current_user)):
    result = await asyncio.to_thread(
        lambda: supabase.table("search_query")
        .select("query_id, created_at, query, paper_url")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return result.data or []
