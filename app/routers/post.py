from typing import List, Optional

from fastapi import Depends, HTTPException, status, Response
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from .. import schemas, models, utils, oauth2

post_router = APIRouter(prefix="/posts", tags=["Posts"])


@post_router.get("", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit=limit)
        .offset(skip)
        .all()
    )

    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .all()
    )
    return results


@post_router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: str, db: Session = Depends(get_db)):
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with given ID: {id}",
        )
    return post


@post_router.post("", response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post: models.Post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@post_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_obj: models.Post = post_query.first()
    if not post_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with given ID: {id}",
        )
    if not post_obj.owner_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized"
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return


@post_router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: str,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_obj: models.Post = post_query.first()
    if not post_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with given ID: {id}",
        )
    if not post_obj.owner_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized"
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
