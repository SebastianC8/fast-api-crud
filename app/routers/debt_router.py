from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.debt_service import DebtService
from app.schemas.debt_schema import CreateDebt, UpdateDebt, DebtResponse, DebtWithUserResponse

router = APIRouter(
    prefix="/debts",
    tags=["debts"]
)

@router.get("/", response_model=list[DebtResponse], status_code=status.HTTP_200_OK)
def get_all_debts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = DebtService(db)
    return service.get_all_debts(skip=skip, limit=limit)

@router.get("/{debt_id}", response_model=DebtWithUserResponse, status_code=status.HTTP_200_OK)
def get_debt_by_id(
    debt_id: int,
    db: Session = Depends(get_db)
):
    service = DebtService(db)
    return service.get_debt_by_id(debt_id)

@router.get("/user/{user_id}", response_model=list[DebtResponse], status_code=status.HTTP_200_OK)
def get_debts_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    service = DebtService(db)
    return service.get_debts_by_user(user_id)

@router.get("/user/{user_id}/unpaid", response_model=list[DebtResponse], status_code=status.HTTP_200_OK)
def get_unpaid_debts_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    service = DebtService(db)
    return service.get_unpaid_debts_by_user(user_id)

@router.post("/", response_model=DebtResponse, status_code=status.HTTP_201_CREATED)
def create_debt(
    debt: CreateDebt,
    db: Session = Depends(get_db)
):
    service = DebtService(db)
    return service.create_debt(debt)

@router.put("/{debt_id}", response_model=DebtResponse, status_code=status.HTTP_200_OK)
def update_debt(
    debt_id: int,
    debt: UpdateDebt,
    db: Session = Depends(get_db)
):
    service = DebtService(db)
    return service.update_debt(debt_id, debt)

@router.delete("/{debt_id}", status_code=status.HTTP_200_OK)
def delete_debt(
    debt_id: int,
    db: Session = Depends(get_db)
):
    service = DebtService(db)
    return service.delete_debt(debt_id)

@router.patch("/{debt_id}/pay", response_model=DebtResponse, status_code=status.HTTP_200_OK)
def mark_debt_as_paid(
    debt_id: int,
    db: Session = Depends(get_db)
):
    service = DebtService(db)
    return service.mark_debt_as_paid(debt_id)