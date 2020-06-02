import unittest
from app import appF, db
from app.models import User


class UserModelCase(unittest.TestCase):
    def setUp(self):
        appF.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='Slava')
        u.set_password('megaslava')
        self.assertFalse(u.check_password('strongP@ss123'))
        self.assertTrue(u.check_password('megaslava'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
