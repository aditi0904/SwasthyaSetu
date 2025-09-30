from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import timedelta
from app.core.config import get_settings
from app.core.security import verify_password, create_access_token, get_password_hash

router = APIRouter()
settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mock user database - replace with real database
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash("admin123"),
        "role": "administrator"
    },
    "doctor": {
        "username": "doctor",
        "hashed_password": get_password_hash("doctor123"), 
        "role": "healthcare_provider"
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    role: str

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    from app.core.security import verify_token
    payload = verify_token(token)
    username = payload.get("sub")
    role = payload.get("role")
    if username is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return User(username=username, role=role)