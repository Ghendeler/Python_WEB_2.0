import datetime
import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.db import engine, get_db
from src.database.models import Base, Contact, User
from src.repository.contacts import (create_contact, get_contact, get_contacts,
                                     get_contacts_by_birthday,
                                     get_contacts_by_str, remove_contact,
                                     update_contact)
from src.schemas import ContactModel


class TestContacts(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(self):
        self.user = User(id=1)
        contacts = [
            Contact(
                name='Jenny',
                surname='Brown',
                email='@test.com',
                birthday=datetime.date(year=1975, month=3, day=27),
                id=1,
                user_id=self.user.id,
            ),
            Contact(
                name='Willy',
                surname='Coreej',
                email='@test.com',
                birthday=datetime.date(year=1982, month=4, day=20),
                id=2,
                user_id=self.user.id,
            ),
            Contact(
                name='Phillip',
                surname='Talor',
                email='www@test.com',
                birthday=datetime.date(year=1975, month=4, day=26),
                id=3,
                user_id=self.user.id,
            ),
            Contact(
                name='Ron',
                surname='Sheeft',
                email='@test.com',
                birthday=datetime.date(year=1962, month=5, day=12),
                id=4,
                user_id=self.user.id,
            ),
        ]
        Contact.__table__.drop(engine)
        # engine.execute("DROP table IF EXISTS contacts")
        # Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.db = next(get_db())
        self.db.add_all(contacts)
        self.db.commit()

    def setUp(self):
        self.session = MagicMock(spec=Session)

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
        result = await get_contacts_by_birthday(days=7, user=self.user, db=self.db)
        self.assertEqual(result[0].id, 3)

    async def test_get_contacts_by_str_found(self):
        result = await get_contacts_by_str(find_str='w', user=self.user, db=self.db)
        res_list = [c.id for c in result]
        self.assertEqual(res_list, [1, 3])


if __name__ == "__main__":
    unittest.main()
