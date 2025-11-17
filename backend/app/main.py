from fastapi import FastAPI
from app.routes import users,search,paper_information, admin
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app = FastAPI()


app.include_router(users.router)
app.include_router(search.router)
app.include_router(paper_information.router)
app.include_router(admin.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "Welcome to the ScholarAI API"}


