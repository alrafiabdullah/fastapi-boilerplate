from sqlalchemy.orm import Session

from utils.user_utils import Hasher

from db.models import User
from db.schema import UserSchema

hasher_obj = Hasher()


def get_user(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserSchema):
    try:
        hashed_password = hasher_obj.get_password_hash(user.password)
        db_user = User(full_name=user.full_name, email=user.email,
                       password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except:
        return None


def update_user(db: Session, user: UserSchema):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        db_user.full_name = user.full_name
        db_user.email = user.email
        db.commit()
        db.refresh(db_user)
        return db_user
    except:
        return None


def delete_user(db: Session, user_id: int):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        db.delete(db_user)
        db.commit()
        return db_user
    except:
        return None


def password_check(plain_password, hashed_password):
    try:
        if not hasher_obj.verify_password(plain_password, hashed_password):
            return False
        return True
    except:
        return False
