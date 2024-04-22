import unittest
from unittest.mock import MagicMock
import datetime

from sqlalchemy.orm import Session

# from src.database.models import Note, Tag, User
from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    get_contacts_by_birthday,
    get_contacts_by_str,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_user_by_email(self):
        ...
