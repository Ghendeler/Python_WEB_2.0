import unittest
# from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.db import engine, get_db
from src.database.models import Base, Contact, User
from src.repository.users import (confirmed_email, create_user,
                                  get_user_by_email, get_user_by_username,
                                  update_avatar, update_token)
from src.schemas import ContactModel, UserModel


class TestUsers(unittest.IsolatedAsyncioTestCase):
    body1 = UserModel(
        username='testguest',
        email='testguest@test.com',
        password='testguest'
    )
    body2 = UserModel(
        username='fixguest',
        email='fixguest@test.com',
        password='fixguest'
    )

    @classmethod
    def setUpClass(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        db = next(get_db())
        self.fix_user = User(**self.body2.dict())
        db.add(self.fix_user)
        db.commit()

    def setUp(self):
        self.session = next(get_db())

    async def test_create_user(self):
        result = await create_user(body=self.body1, db=self.session)
        user = User(**self.body1.dict())
        user.id = 2
        self.assertEqual(result.id, user.id)

    async def test_get_user_by_email_found(self):
        user_email = self.body2.email
        result = await get_user_by_email(email=user_email, db=self.session)
        self.assertEqual(result.email, user_email)

    async def test_get_user_by_email_not_found(self):
        user_email = 'notetestguest@test.com'
        result = await get_user_by_email(email=user_email, db=self.session)
        self.assertIsNone(result)

    async def test_get_user_by_username_found(self):
        username = self.body2.username
        result = await get_user_by_username(username=username, db=self.session)
        self.assertEqual(result.username, username)

    async def test_get_user_by_username_not_found(self):
        username = 'notetestguest@test.com'
        result = await get_user_by_username(username=username, db=self.session)
        self.assertIsNone(result)

    async def test_confirmed_email(self):
        user_email = self.body2.email
        result = await confirmed_email(email=user_email, db=self.session)
        user_from_db = await get_user_by_email(email=user_email, db=self.session)
        self.assertIsNone(result)
        self.assertEqual(user_from_db.confirmed, True)

    async def test_update_token(self):
        token_string = "jnLkj_klkljNkBhb466hfyi,56b546Gb54g6opOIjbgBB"
        result = await update_token(user=self.fix_user, token=token_string, db=self.session)
        self.assertEqual(result.refresh_token, token_string)

    async def test_update_avatar(self):
        email = self.body2.email
        avatar_url = "https:///cloudinary.com//id=JhHfcRDtC"
        result = await update_avatar(email=email, url=avatar_url, db=self.session)
        self.assertEqual(result.avatar, avatar_url)
