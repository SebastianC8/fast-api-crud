# Schema BASE: atributos comunes
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

# Schema BASE: atributos comunes
class UserBase(BaseModel):
    email: EmailStr  # Valida que sea un email válido
    nombre: str
    apellido: str

# Schema para CREAR usuario
class CreateUser(UserBase):
    pass

# Schema para actualizar usuario
class UpdateUser(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    is_active: Optional[bool] = None

# Schema para RESPUESTA (lo que devuelve el API)
class UserResponse(UserBase):
    id: int
    is_active: bool
    email: EmailStr
    nombre: str
    apellido: str

class UserNameResponse(BaseModel):
    fullName: str

class UserStatusResponse(BaseModel):
    id: int
    fullName: str
    is_active: bool

class Config:
    model_config = ConfigDict(from_attributes=True) # Permite convertir desde ORM models