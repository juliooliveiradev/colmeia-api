import os
import sys
import threading
import webbrowser
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.routers import auth, dashboard, harvests, hives, inspections
from app.seed import seed_if_empty

SWAGGER_URL = "http://127.0.0.1:8000/docs"


def _running_in_docker() -> bool:
    return Path("/.dockerenv").exists() or os.getenv("RUNNING_IN_DOCKER") == "1"


def _should_open_swagger() -> bool:
    if _running_in_docker():
        return False
    if os.getenv("COLMEIA_OPEN_BROWSER", "1").lower() in {"0", "false", "no"}:
        return False
    if "--reload" in sys.argv:
        flag = Path("data/.swagger_reload")
        parent_pid = str(os.getppid())
        if flag.exists() and flag.read_text(encoding="utf-8").strip() == parent_pid:
            return False
        flag.parent.mkdir(parents=True, exist_ok=True)
        flag.write_text(parent_pid, encoding="utf-8")
    return True


def _open_swagger_in_browser() -> None:
    if _should_open_swagger():
        webbrowser.open(SWAGGER_URL)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()
    threading.Timer(1.0, _open_swagger_in_browser).start()
    yield


app = FastAPI(
    title=settings.app_name,
    description=(
        "API REST para gestão de apiários urbanos: colmeias, revisões de campo, "
        "colheitas de mel e indicadores do painel comunitário."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(hives.router)
app.include_router(inspections.router)
app.include_router(harvests.router)
app.include_router(dashboard.router)


@app.get("/api/health", tags=["Saúde"])
def health():
    return {"status": "ok", "service": settings.app_name}
