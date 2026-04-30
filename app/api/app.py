from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.database import init_db

app = FastAPI(
    title="YKZZ Quant API",
    description="A股可转债策略研究工具 API",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(router, prefix="/api")


@app.on_event("startup")
async def startup():
    init_db()


@app.get("/")
async def root():
    return {"message": "YKZZ Quant API", "version": "0.1.0"}
