from fastapi import FastAPI
from app.routes import users,search,paper_information, admin

app = FastAPI()

app.include_router(users.router)
app.include_router(search.router)
app.include_router(paper_information.router)
app.include_router(admin.router)

@app.get("/")
async def home():
    return {"message": "Welcome to the ScholarAI API"}


