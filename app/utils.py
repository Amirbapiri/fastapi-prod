from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(raw_password: str):
    return pwd_context.hash(raw_password)


def verify(raw_password, hashed_password):
    return pwd_context.verify(raw_password, hashed_password)
