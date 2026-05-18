import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import logging

logger = logging.getLogger("Clinica-LENS-Auth")

# Configuration for Enterprise JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# In an enterprise system, authentication is delegated to an IdP (e.g., Keycloak, Auth0, Okta).
# We simulate the token verification endpoint which validates JWTs issued by the federated IdP.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    role: str # radiologist, admin, etc.
    tenant_id: str # Multi-tenant isolation

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    # Simulated fallback for legacy token endpoint (Production uses OIDC flow via UI)
    logger.warning("Using legacy authentication endpoint. Migrate to OIDC IdP.")
    if password == "clinica-lens-2026":
        return User(username=username, full_name="Dr. " + username, role="radiologist", tenant_id="default_tenant")
    return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    # Inject enterprise claims
    to_encode.update({
        "tenant_id": "default_tenant", # Would be fetched from OIDC claims
        "iss": "clinica-lens-idp",
        "aud": "clinica-lens-api"
    })
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Validates the JWT token. In an enterprise setting, this relies on JWKS 
    from the OIDC provider rather than a symmetric local SECRET_KEY.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Note: Production systems use jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        tenant_id: str = payload.get("tenant_id")
        
        if username is None or tenant_id is None:
            raise credentials_exception
            
        return User(
            username=username,
            tenant_id=tenant_id,
            role=payload.get("role", "user")
        )
    except JWTError as e:
        logger.error(f"JWT Validation Error: {e}")
        raise credentials_exception
