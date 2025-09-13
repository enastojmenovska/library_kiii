from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import check_db_connection, init_db
from .routers import authors as authors_router
from .routers import genres as genres_router
from .routers import books as books_router

app = FastAPI(title="Library API", version="0.1.0")

# allow your dev frontend origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health/liveness")
def liveness():
    return {"status": "ok"}

@app.get("/health/readiness")
def readiness():
    try:
        check_db_connection()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "fail", "detail": str(e)}

app.include_router(authors_router.router)
app.include_router(genres_router.router)
app.include_router(books_router.router)
