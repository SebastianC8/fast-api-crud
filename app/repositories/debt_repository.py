from sqlalchemy.orm import Session
from typing import Optional
from app.models.debt_model import Debt
from app.schemas.debt_schema import CreateDebt, UpdateDebt

class DebtRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> list[Debt]:
        return self.db.query(Debt).offset(skip).limit(limit).all()
    
    def get_by_id(self, debt_id: int) -> Optional[Debt]:
        return self.db.query(Debt).filter(Debt.id == debt_id).first()
    
    def get_by_user_id(self, user_id: int) -> list[Debt]:
        return self.db.query(Debt).filter(Debt.user_id == user_id).all()
    
    def get_unpaid_by_user(self, user_id: int) -> list[Debt]:
        return self.db.query(Debt).filter(Debt.user_id == user_id, Debt.status == False).all()
    
    def create(self, debt_data: CreateDebt) -> Debt:
        db_debt = Debt(**debt_data.model_dump())
        self.db.add(db_debt)
        self.db.commit()
        self.db.refresh(db_debt)
        return db_debt
    
    def update(self, debt_id: int, debt_data: UpdateDebt) -> Optional[Debt]:
        db_debt = self.get_by_id(debt_id)

        if not db_debt:
            return None
        
        update_data = debt_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_debt, field, value)
        
        self.db.commit()
        self.db.refresh(db_debt)
        return db_debt
    
    def delete(self, debt_id: int) -> bool:
        db_debt = self.get_by_id(debt_id)

        if not db_debt:
            return False
        
        self.db.delete(db_debt)
        self.db.commit()
        return True
    
    def mark_as_paid(self, debt_id: int) -> Optional[Debt]:
        db_debt = self.get_by_id(debt_id)

        if not db_debt:
            return None
        
        db_debt.status = True
        self.db.commit()
        self.db.refresh(db_debt)
        
        return db_debt