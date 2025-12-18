from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


class Debt(Base):
    __tablename__ = "debts"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="debts")

    def __repr__(self):
        return f"<Debt(id={self.id}, description={self.description}, value={self.value}, date={self.date}, status={self.status})>"
