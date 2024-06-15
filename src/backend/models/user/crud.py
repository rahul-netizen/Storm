from sqlalchemy.orm import Session
from models.user import user_models, user_schemas
from utils.authentication import get_password_hash


def get_user_by_username(db: Session, username: str):
    return db.query(user_models.User).filter(user_models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: user_schemas.UserCreate):
    db_user = user_models.User(
        username = user.username,
        hashed_password = get_password_hash(user.hashed_password),
        email = user.email,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user