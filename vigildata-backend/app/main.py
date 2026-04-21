from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base, SessionLocal
from app.models import usuario as _u, incidente as _i  # noqa: ensure models are registered
from app.routers import auth, incidentes


def _seed_admin():
    from passlib.context import CryptContext
    from app.models.usuario import Usuario, Rol

    db = SessionLocal()
    try:
        existe = db.query(Usuario).filter(Usuario.email == "admin@vigildata.cl").first()
        if not existe:
            pwd = CryptContext(schemes=["bcrypt"], deprecated="auto").hash("admin123")
            db.add(Usuario(email="admin@vigildata.cl", password=pwd, rol=Rol.ANALISTA))
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    _seed_admin()
    yield


app = FastAPI(
    title="VigilData API",
    description="API REST para mapa colaborativo de seguridad ciudadana",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(incidentes.router)


@app.get("/")
def root():
    return {"status": "ok", "proyecto": "VigilData"}
