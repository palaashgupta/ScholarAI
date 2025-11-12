import asyncio
from fastapi import APIRouter
from app.supabase_client import supabase

router = APIRouter(prefix="/papers", tags=["Papers"])

# ---------------------
# Store paper info
# ---------------------
async def store_paper(paper: dict):
    """
    Insert paper into paper_information if not exists
    """
    try:
        existing = await asyncio.to_thread(
            lambda: supabase.table("paper_information")
            .select("paper_id")
            .eq("paper_url", paper["paper_url"])
            .execute()
        )
        if existing.data:
            return existing.data[0]

        result = await asyncio.to_thread(
            lambda: supabase.table("paper_information").insert({
                "title": paper.get("title") or "No Title",
                "created_at": str(paper["created_at"]),
                "authors": paper["authors"],
                "summary": paper["summary"],
                "paper_url": paper["paper_url"],
                "published_in": paper["published_in"]
            }).execute()
        )
        return result.data[0] if result.data else None
    except:
        return None


# ---------------------
# Get papers by URLs
# ---------------------
async def get_papers_by_urls(urls: list):
    if not urls:
        return []

    result = await asyncio.to_thread(
        lambda: supabase.table("paper_information")
        .select("title,paper_id, created_at, authors, summary, paper_url, published_in")
        .in_("paper_url", urls)
        .execute()
    )
    return result.data or []


# ---------------------
# Get single paper by ID
# ---------------------
@router.get("/paper/{paper_id}")
async def get_paper(paper_id: int):
    result = await asyncio.to_thread(
        lambda: supabase.table("paper_information")
        .select("*")
        .eq("paper_id", paper_id)
        .execute()
    )
    if not result.data:
        return {"error": "Paper not found"}
    return result.data[0]

### Filter paper by Authors
@router.get("/authors/{author_name}")
async def get_papers_by_author(author_name: str):
    result = await asyncio.to_thread(
        lambda: supabase.table("paper_information")
        .select("*")
        .contains("authors", [author_name])
        .execute()
    )
    if not result.data:
        return {"error": "No papers found for the given author"}
    return result.data

### Filter paper by Publish date
@router.get("/created_at/{date}")
async def get_papers_by_date(date: str):
    result = await asyncio.to_thread(
        lambda: supabase.table("paper_information")
        .select("*")
        .eq("created_at", date)
        .execute()
    )
    if not result.data:
        return {"error": "No papers found for the given date"}
    return result.data

### Filter papers by Published In
@router.get("/published_in/{venue}")
async def get_papers_by_venue(venue: str):
    result = await asyncio.to_thread(
        lambda: supabase.table("paper_information")
        .select("*")
        .contains("published_in", [venue])
        .execute()
    )
    if not result.data:
        return {"error": "No papers found for the given venue"}
    return result.data