from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, UTC

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    belvo_links = relationship("BelvoLink", back_populates="user")

class BelvoLink(Base):
    __tablename__ = "belvo_links"
    
    id = Column(String, primary_key=True, index=True)  
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) 
    institution = Column(String, index=True)
    external_id = Column(String, nullable=True)
    access_mode = Column(String) 
    status = Column(String)  
    institution_user_id = Column(String, nullable=True)
    fetch_resources = Column(JSON)  
    created_at = Column(DateTime, default=datetime.now(UTC))
    last_accessed_at = Column(DateTime, nullable=True)
    credentials_storage = Column(String, nullable=True)
    stale_in = Column(String, nullable=True)
    
    user = relationship("User", back_populates="belvo_links")