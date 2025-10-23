from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(100), nullable=False )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Reverse relationship
    images = relationship("Image", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"id: {self.id} -> username: {self.username}"

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    url = Column(String(100), nullable=False)
    meta_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="images")

    def __repr__(self) -> str:
        return f"id: {self.id} -> url: {self.url}"