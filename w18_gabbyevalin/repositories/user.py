
from sqlalchemy import ScalarResult
from w18_gabbyevalin import db
from w18_gabbyevalin.model import User


def user_list() -> ScalarResult[User]:
    return db.session.execute(
        db.select(User).order_by(User.id)).scalars()


def user_by_id(id: int) -> User:
    try:
        return db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
    except:
        return None


def user_by_email(email: str) -> User:
    try:
        return db.session.execute(db.select(User).filter_by(email=email)).scalar_one()
    except:
        return None


def user_create(email: str, name: str, password: str) -> User:
    try:
        user = User(
            email=email,
            name=name,
        )
        if password.strip() == "":
            raise
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    except:
        return None


def user_update(user: User, name: str) -> User:
    try:
        user.name = name
        db.session.commit()
        return user
    except:
        return None


def user_change_password(user: User, password: str) -> User:
    try:
        if password.strip() == "":
            raise
        user.set_password(password)
        db.session.commit()
        return user
    except:
        return None


def user_delete(user: User) -> bool:
    try:
        db.session.delete(user)
        db.session.commit()
        return True
    except:
        return False
