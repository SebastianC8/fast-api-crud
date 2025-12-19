from typing import Optional
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import CreateUser, UpdateUser, UserStatusResponse

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_active_users(self) -> list[User]:
        return self.db.query(User).filter(User.is_active == True).all()
    
    def changeStatus(self, user_id: int) -> Optional[User]:
        db_user = self.get_by_id(user_id)

        if not db_user:
            return None
        
        db_user.is_active = not db_user.is_active

        self.db.commit()
        self.db.refresh(db_user)

        return db_user
    
    def create(self, user_data: dict) -> User:

        # Crear User desde dict usando **
        user = User(**user_data)
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def update(self, user_id: int, user_data: UpdateUser) -> Optional[User]:

        db_user = self.get_by_id(user_id)

        if not db_user:
            return None
        
        # Convertir Pydantic model a dict, excluyendo campos None
        update_data = user_data.model_dump(exclude_unset=True)
        
        # Actualizar solo los campos presentes
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id: int) -> bool:
        
        db_user = self.get_by_id(user_id)

        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True