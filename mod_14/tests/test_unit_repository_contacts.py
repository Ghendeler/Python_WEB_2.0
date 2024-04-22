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

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contac_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(
            name="test",
            surname="test1",
            email=None,
            phone="0151054684351",
            birthday="1985-05-05",
            note=None,
        )
        self.session.query().filter().all.return_value = Contact()
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.note, body.note)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactModel(
            name="test",
            surname="test1",
            email=None,
            phone="0151054684351",
            birthday="1985-05-05",
            note=None,
        )
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(
            contact_id=1, body=body, user=self.user, db=self.session
        )
        self.assertEqual(result, contact)
        self.assertEqual(result.user_id[0], self.user.id)

    async def test_update_contact_not_found(self):
        body = ContactModel(
            name="test",
            surname="test1",
            email=None,
            phone="0151054684351",
            birthday="1985-05-05",
            note=None,
        )
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(
            contact_id=1, body=body, user=self.user, db=self.session
        )
        self.assertEqual(result, None)

    async def test_get_contacts_by_birthday_found(self):
        contacts = [
            Contact(birthday=datetime.date(y=1975, m=3, d=27), id=1),
            Contact(birthday=datetime.date(y=1982, m=4, d=20), id=2),
            Contact(birthday=datetime.date(y=1975, m=4, d=25), id=3),
            Contact(birthday=datetime.date(y=1962, m=5, d=12), id=4),
        ]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_birthday(days=7, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_str_found(self):
        # get_contacts_by_str(find_str: str, user: User, db: Session)
        ...


if __name__ == "__main__":
    unittest.main()
