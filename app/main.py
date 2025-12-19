# app/main.py
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth_router, debt_router, user_router
from fastapi.middleware.cors import CORSMiddleware

# Crear las tablas en la base de datos
# Esto ejecuta el CREATE TABLE si la tabla no existe
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="CRUD API con FastAPI",
    description="API RESTful con arquitectura en capas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8100"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
# Esto registra todos los endpoints de user_router
app.include_router(user_router.router)
app.include_router(debt_router.router)
app.include_router(auth_router.router);

# Endpoint raíz (opcional)
@app.get("/")
def root():
    """
    Endpoint de bienvenida
    """
    return {
        "message": "Bienvenido a la API de usuarios",
        "docs": "/docs",
        "redoc": "/redoc"
    }