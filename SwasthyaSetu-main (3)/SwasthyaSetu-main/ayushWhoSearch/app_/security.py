import os, requests
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

load_dotenv()
ABHA_INTROSPECT = os.getenv("ABHA_INTROSPECT")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def validate_abha_token(token: str):
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    if token.lower().startswith("bearer "):
        token = token.split(" ",1)[1]
    if ABHA_INTROSPECT:
        r = requests.post(ABHA_INTROSPECT, data={"token": token}, timeout=5)
        if r.status_code != 200 or not r.json().get("active"):
            raise HTTPException(status_code=401, detail="Invalid ABHA token")
        return r.json()
    # demo fallback
    if token.startswith("demo-abha:"):
        return {"active": True, "sub": token.split(":",1)[1]}
    return {"active": True, "sub":"unknown"}
