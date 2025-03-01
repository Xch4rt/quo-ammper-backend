from pydantic import BaseModel
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



class BelvoLinkCreate(BaseModel):
    id: str  # ID del link proporcionado por Belvo
    institution: str
    external_id: Optional[str] = None
    access_mode: str  # "single" o "recurrent"
    status: str
    institution_user_id: Optional[str] = None
    fetch_resources: Optional[List[str]] = []
    created_at: Optional[datetime] = None
    last_accessed_at: Optional[datetime] = None
    credentials_storage: Optional[str] = None
    stale_in: Optional[str] = None
