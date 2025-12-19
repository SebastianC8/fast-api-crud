from app.database import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

class User(Base):
    # Nombre de la tabla
    __tablename__ = "users"

    # Columnas de la tabla
    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, index = True, nullable = False)
    nombre = Column(String, nullable = False)
    apellido = Column(String, nullable = False)
    password = Column(String, nullable=False) 
    is_active = Column(Boolean, default = True)

    debts = relationship("Debt", back_populates = "user", cascade="all, delete-orphan")

    # toString()
    def __repr__(self):
        """Representación legible del objeto (útil para debugging)"""
        return f"<User(id={self.id}, email={self.email}, nombre={self.nombre})>"