# -*- coding: utf-8 -*-
"""
Modulo de autenticacao JWT para a API
Autores:
 357103 - Víctor Kennedy Kaneko Nunes
 358078 - Octavio Ribeiro
 360075 - Gabriel Oliveira
 358032 - Lucas Guilherme Mordaski
Data: 2025

Implementa autenticacao JWT para proteger endpoints da API.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Importar configuracoes
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Configuracao do contexto de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Usuarios fake para demonstracao (em producao usar banco de dados)
# Senha: "quantumfinance123" para todos
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Administrador QuantumFinance",
        "email": "admin@quantumfinance.com",
        "hashed_password": "$2b$12$G8SP8eoLCLC91VvHVRJ1.ePzzFldmqoACzSJud1//pvWKZCu8htkK",
        "disabled": False,
    },
    "analista": {
        "username": "analista",
        "full_name": "Analista de Credito",
        "email": "analista@quantumfinance.com",
        "hashed_password": "$2b$12$G8SP8eoLCLC91VvHVRJ1.ePzzFldmqoACzSJud1//pvWKZCu8htkK",
        "disabled": False,
    }
}

# Modelos Pydantic
class Token(BaseModel):
    """Modelo para resposta de token."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Dados do token."""
    username: Optional[str] = None

class User(BaseModel):
    """Modelo de usuario."""
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    """Usuario no banco com senha hash."""
    hashed_password: str

def verify_password(plain_password, hashed_password):
    """Verifica se a senha esta correta."""
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    """Busca usuario no banco."""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    """Autentica usuario."""
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria token de acesso JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Obtem usuario atual do token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Verifica se usuario esta ativo."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user