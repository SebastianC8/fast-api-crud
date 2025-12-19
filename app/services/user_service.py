# app/services/user_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUser, PostResponse, UpdateUser, UserResponse, UserNameResponse, UserStatusResponse
from app.infrastructure.external_api import external_api_client
from app.core.security import get_password_hash

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = self.repository.get_all(skip=skip, limit=limit)
        # Convertir cada User (SQLAlchemy) a UserResponse (Pydantic)
        return [
            UserResponse(
                id=user.id,
                email=user.email,
                nombre=user.nombre,
                apellido=user.apellido,
                is_active=user.is_active
            ) 
        for user in users
    ]
    
    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        
        # Validación de negocio: el usuario debe existir
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        
        return UserResponse (
            id=user.id,
            email=user.email,
            nombre=user.nombre,
            apellido=user.apellido,
            is_active=user.is_active
        )
    
    async def get_all_posts(self) -> List[PostResponse]:
        posts = await external_api_client.get_all_posts()
        if not posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron posts"
            )
        return posts
    
    async def get_post_by_id(self, post_id: int) -> PostResponse:
        post = await external_api_client.get_post_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post con ID {post_id} no encontrado"
            )
        return post
    
    def get_active_users(self) -> List[UserNameResponse]:
        users = self.repository.get_active_users()
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron usuarios activos"
            )
        
        return [
            UserNameResponse(
                fullName=f"{user.nombre} {user.apellido}"
            )
            for user in users
        ]
    
    def change_user_status(self, user_id: int) -> UserStatusResponse:
        user_db = self.repository.get_by_id(user_id)
        
        # Validación de negocio: el usuario debe existir
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        
        user_db = self.repository.changeStatus(user_id)

        return UserStatusResponse (
            id=user_db.id,
            fullName=f"{user_db.nombre} {user_db.apellido}",
            is_active=user_db.is_active
        )

    def create_user(self, user_data: CreateUser) -> UserResponse:

        # Validación de negocio: email único
        existing_user = self.repository.get_by_email(user_data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El email {user_data.email} ya está registrado"
            )
        
        # Convertir Pydantic model a dict
        user_dict = user_data.model_dump()  # ← user_data, no user
        
        # Hashear password
        user_dict['password'] = get_password_hash(user_dict['password'])
        
        # Crear usuario en BD
        user = self.repository.create(user_dict)
        
        return UserResponse (
            id=user.id,
            email=user.email,
            nombre=user.nombre,
            apellido=user.apellido,
            is_active=user.is_active
        )
    
    def update_user(self, user_id: int, user_data: UpdateUser) -> UserResponse:

        # Validación: si se intenta cambiar el email
        if user_data.email:
            existing_user = self.repository.get_by_email(user_data.email)
            # El email existe Y pertenece a otro usuario
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El email {user_data.email} ya está registrado"
                )
        
        # Intentar actualizar
        user = self.repository.update(user_id, user_data)
        
        # Validación: el usuario debe existir
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        
        return UserResponse (
            id=user.id,
            email=user.email,
            nombre=user.nombre,
            apellido=user.apellido,
            is_active=user.is_active
        )
    
    def delete_user(self, user_id: int) -> dict:
        deleted = self.repository.delete(user_id)
        
        # Validación: el usuario debe existir
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        
        return {"message": f"Usuario con ID {user_id} eliminado exitosamente"}