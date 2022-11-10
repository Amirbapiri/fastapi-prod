from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import utils, oauth2
from app.database import get_db
from app.models import User
from app.schemas import UserLogin, Token

auth_router = APIRouter(tags=["Authentication"])


@auth_router.post("/login", response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No user found with the given credentials",
        )
    verified = utils.verify(user_credentials.password, user.password)
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )
    # Create JWT
    token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "Bearer"}
