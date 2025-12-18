# app/routers/user_router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user_schema import CreateUser, UpdateUser, UserNameResponse, UserResponse, UserStatusResponse

# Crear el router
router = APIRouter(prefix = "/users", tags = ["users"])

@router.get("/", response_model = List[UserResponse], status_code = status.HTTP_200_OK)
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_all_users(skip = skip, limit = limit)

@router.get("/activeUsers", response_model = List[UserNameResponse], status_code = status.HTTP_200_OK)
def get_active_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_active_users()

@router.get("/{user_id}", response_model = UserResponse, status_code = status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user_by_id(user_id)

@router.post("/", response_model = UserResponse, status_code = status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create_user(user)

@router.put("/{user_id}", response_model = UserResponse, status_code = status.HTTP_200_OK)
def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.update_user(user_id, user)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.delete_user(user_id)

@router.post("/changeStatus/{user_id}", response_model = UserStatusResponse, status_code = status.HTTP_200_OK)
def change_user_status(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.change_user_status(user_id)