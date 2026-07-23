# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import admin, auth, requests, universities, blog, dashboard

app = FastAPI(
    title="GoCanadaBR Consultoria",
    version="1.0.0",
    docs_url="/docs" if True else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.gocanadabr.com.br"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(universities.router)
app.include_router(requests.router)
app.include_router(admin.router)
app.include_router(blog.router)
app.include_router(dashboard.router)


@app.get("/health")
def health():
    return {"status": "ok"}