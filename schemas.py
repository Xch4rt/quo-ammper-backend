from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class User(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True

class BelvoLinkCreate(BaseModel):
    id: str = Field(..., alias="link")
    institution: str
    external_id: Optional[str] = None
    access_mode: Optional[str] = "single"  # Valor predeterminado o ajústalo según necesites
    status: Optional[str] = "active"       # Valor predeterminado o ajústalo según necesites
    institution_user_id: Optional[str] = None
    fetch_resources: Optional[List[str]] = []
    created_at: Optional[datetime] = None
    last_accessed_at: Optional[datetime] = None
    credentials_storage: Optional[str] = None
    stale_in: Optional[str] = None

    class Config:
        allow_population_by_field_name = True