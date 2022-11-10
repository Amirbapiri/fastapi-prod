from fastapi import status, Depends, HTTPException, Response
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, models, utils


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut,
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with the given email '{user.email}' already exists",
        )
    hashed_password = utils.hash(user.password)

    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@user_router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with given ID: {id}",
        )
    return user
