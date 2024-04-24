# from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Fetches a user from the database by their email.

    :param email:str: The email of the user to fetch.
    :param db:Session: The database session.
    :return:User: The fetched user.
    """
    return db.query(User).filter(User.email == email).first()


async def get_user_by_username(username: str, db: Session) -> User:
    """
    Fetches a user from the database by their username.

    :param username:str: The username of the user to fetch.
    :param db:Session: The database session.
    :return:User: The fetched user.
    """
    return db.query(User).filter(User.username == username).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user in the database.

    :param body:UserModel: The data of the user to create.
    :param db:Session: The database session.
    :return:User: The created user.
    """
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirms the email of a user in the database.

    :param email:str: The email of the user to confirm.
    :param db:Session: The database session.
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates the token of a user in the database.

    :param user:User: The user to update the token of.
    :param token:str | None: The new token.
    :param db:Session: The database session.
    """
    user.refresh_token = token
    db.commit()
    return user


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Updates the avatar of a user in the database.

    :param email:str: The email of the user to update the avatar of.
    :param url:str: The new avatar URL.
    :param db:Session: The database session.
    :return:User: The updated user.
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
