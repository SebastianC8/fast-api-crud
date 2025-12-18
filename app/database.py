from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Crear el "motor" de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args = { "check_same_thread": False }
)

# 2. SESSION: Crea sesiones para hacer operaciones en la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. BASE: Clase base para todos los modelos
Base = declarative_base()

# 4. DEPENDENCY: Función que FastAPI usará para obtener la sesión
# Esta función se ejecuta en cada request. Abre una sesión, la usa, y la cierra al terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()