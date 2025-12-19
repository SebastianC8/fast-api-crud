# Schema BASE: atributos comunes
from typing import Optional
from pydantic import Field, BaseModel, ConfigDict, EmailStr, field_validator

# Schema BASE: atributos comunes
class UserBase(BaseModel):
    email: EmailStr  # Valida que sea un email válido
    nombre: str
    apellido: str

# Schema para CREAR usuario
class CreateUser(UserBase):
    # pass

    email: EmailStr
    
    nombre: str = Field(
        min_length=3,
        max_length=20,
        description="El nombre debe tener entre 3 y 20 caracteres"
    )

    apellido: str = Field(
        min_length=3,
        max_length=20,
        description="El apellido debe tener entre 3 y 5 caracteres",
    )

    password: str = Field(
        min_length=8,
        max_length=100,
        description="Contraseña segura (mínimo 8 caracteres)"
    )

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Debe contener al menos una mayúscula")
        if not any(c.islower() for c in v):
            raise ValueError("Debe contener al menos una minúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("Debe contener al menos un número")
        return v

    # @field_validator("nombre")
    # @classmethod
    # def nombre_must_be_alpha(cls, value):
    #     if not value.isalpha():
    #         raise ValueError("El nombre solo debe contener letras")
    #     return value

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

class PostResponse(BaseModel):
    userId: int
    id: int
    title: str
    body: str

class Config:
    model_config = ConfigDict(from_attributes=True) # Permite convertir desde ORM models