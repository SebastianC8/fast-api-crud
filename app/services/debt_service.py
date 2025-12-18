from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.debt_repository import DebtRepository
from app.repositories.user_repository import UserRepository
from app.schemas.debt_schema import CreateDebt, UpdateDebt, DebtResponse, DebtWithUserResponse

class DebtService:
    
    def __init__(self, db: Session):
        self.repository = DebtRepository(db)
        self.user_repository = UserRepository(db)
    
    def get_all_debts(self, skip: int = 0, limit: int = 100) -> list[DebtResponse]:
        debts = self.repository.get_all(skip=skip, limit=limit)
        return [
            DebtResponse(
                id=debt.id,
                description=debt.description,
                value=debt.value,
                date = debt.date,
                status=debt.status,
                user_id=debt.user_id
            )
            for debt in debts
        ]
    
    def get_debt_by_id(self, debt_id: int) -> DebtWithUserResponse:
        debt = self.repository.get_by_id(debt_id)
        if not debt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Deuda con ID {debt_id} no encontrada"
            )
        
        return DebtWithUserResponse(
            id=debt.id,
            description=debt.description,
            value=debt.value,
            date = debt.date,
            status=debt.status,
            user_id=debt.user_id,
            user_nombre=debt.user.nombre,
            user_apellido=debt.user.apellido,
            user_email=debt.user.email
        )
    
    def get_debts_by_user(self, user_id: int) -> list[DebtResponse]:
        # Validar que el usuario existe
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        
        debts = self.repository.get_by_user_id(user_id)
        return [
            DebtResponse(
                id=debt.id,
                description=debt.description,
                value=debt.value,
                date = debt.date,
                status=debt.status,
                user_id=debt.user_id
            )
            for debt in debts
        ]
    
    def get_unpaid_debts_by_user(self, user_id: int) -> list[DebtResponse]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        
        debts = self.repository.get_unpaid_by_user(user_id)
        return [
            DebtResponse(
                id=debt.id,
                description=debt.description,
                value=debt.value,
                date = debt.date,
                status=debt.status,
                user_id=debt.user_id
            )
            for debt in debts
        ]
    
    def create_debt(self, debt_data: CreateDebt) -> DebtResponse:
        # Validar que el usuario existe
        user = self.user_repository.get_by_id(debt_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {debt_data.user_id} no encontrado"
            )
        
        debt = self.repository.create(debt_data)
        return DebtResponse(
            id=debt.id,
            description=debt.description,
            value=debt.value,
            date = debt.date,
            status=debt.status,
            user_id=debt.user_id
        )
    
    def update_debt(self, debt_id: int, debt_data: UpdateDebt) -> DebtResponse:
        existing_debt = self.repository.get_by_id(debt_id)
        if not existing_debt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Deuda con ID {debt_id} no encontrada"
            )
        
        if debt_data.user_id:
            user = self.user_repository.get_by_id(debt_data.user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Usuario con ID {debt_data.user_id} no encontrado"
                )
            
        debt = self.repository.update(debt_id, debt_data)
        
        return DebtResponse(
            id=debt.id,
            description=debt.description,
            value=debt.value,
            date = debt.date,
            status=debt.status,
            user_id=debt.user_id
        )
    
    def delete_debt(self, debt_id: int) -> dict:
        deleted = self.repository.delete(debt_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Deuda con ID {debt_id} no encontrada"
            )
        
        return {"message": f"Deuda con ID {debt_id} eliminada exitosamente"}
    
    def mark_debt_as_paid(self, debt_id: int) -> DebtResponse:
        debt = self.repository.mark_as_paid(debt_id)
        if not debt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Deuda con ID {debt_id} no encontrada"
            )
        
        return DebtResponse(
            id=debt.id,
            description=debt.description,
            value=debt.value,
            date = debt.date,
            status=debt.status,
            user_id=debt.user_id
        )