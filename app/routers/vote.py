from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import oauth2, models, database
from app.schemas import Vote

vote_router = APIRouter(prefix="/vote", tags=["Vote"])


@vote_router.post("/", status_code=status.HTTP_200_OK)
def vote(
    vote: Vote,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {vote.post_id} does not exist",
            )
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id,
    )
    found_vote = vote_query.first()
    if vote.vote_dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on post {found_vote.post_id}",
            )
        new_vote = models.Vote(
            post_id=vote.post_id,
            user_id=current_user.id,
        )
        db.add(new_vote)
        db.commit()
        # return {"message": "voted successfully"}
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Couldn't find any vote"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_202_ACCEPTED)
