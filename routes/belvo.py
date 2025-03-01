from fastapi import APIRouter, Depends, HTTPException, status
import httpx
import os
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from models import BelvoLink, User  
from schemas import BelvoLinkCreate  
from database import SessionLocal, get_db
from auth import verify_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    
@router.get("/banks")
async def get_banks(token: str = Depends(oauth2_scheme)):
    verified_token = verify_token(token)
    
    BELVO_BASE_URL = os.getenv("BELVO_BASE_URL")
    BELVO_SECRET_ID = os.getenv("BELVO_SECRET_ID")
    BELVO_SECRET_PASSWORD = os.getenv("BELVO_SECRET_PASSWORD")
    
    headers = {
        "Content-Type": "application/json",
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BELVO_BASE_URL}/accounts",
            auth=(BELVO_SECRET_ID, BELVO_SECRET_PASSWORD),
            headers=headers,
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
@router.get("/balance")
async def get_balance(token: str = Depends(oauth2_scheme)):
    verified_token = verify_token(token)
    
    BELVO_BASE_URL = os.getenv("BELVO_BASE_URL")
    BELVO_SECRET_ID = os.getenv("BELVO_SECRET_ID")
    BELVO_SECRET_PASSWORD = os.getenv("BELVO_SECRET_PASSWORD")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BELVO_BASE_URL}/transactions/",
            auth=(BELVO_SECRET_ID, BELVO_SECRET_PASSWORD)
        )
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
        
    transactions = response.json()
        
    incomes = sum(item["amount"] for item in transactions if item["amount"] > 0)
    expenses = sum(item["amount"] for item in transactions if item["amount"] < 0)
    balance = incomes - expenses
    return {
        "incomes": incomes,
        "expenses": expenses,
        "balance": balance,
        "transactions": transactions
    }
        
        
@router.post("/belvo/links", status_code=status.HTTP_201_CREATED)
async def create_belvo_link(
    link_data: BelvoLinkCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    username = verify_token(token)
    
    user = db.query(User).filter(User.email == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_link = BelvoLink(
        id = link_data.id,
        user_id = user.id,
        institution = link_data.institution,
        external_id = link_data.external_id,
        access_mode = link_data.access_mode,
        status = link_data.status,
        institution_user_id = link_data.institution_user_id,
        fetch_resources = link_data.fetch_resources,
        created_at = link_data.created_at or None,
        last_accessed_at = link_data.last_accessed_at or None,
        credentials_storage = link_data.credentials_storage,
        stale_in = link_data.stale_in
    )
    
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    
    return new_link
