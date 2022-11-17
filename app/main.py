from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models
from app.routers import post, user, auth, vote

# models.Base.metadata.drop_all()
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(post.post_router)
app.include_router(user.user_router)
app.include_router(auth.auth_router)
app.include_router(vote.vote_router)


@app.get("/")
def root():
    return {"message": "Hi see the /docs."}
