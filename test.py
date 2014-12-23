import unittest
from app import db
from models import User, Room
import os

class KFCTestCase(unittest.TestCase):
  def setUp(self):
    db.create_all()

  def test_not_exist_user(self):
    user = User.query.filter_by(username='unko').first()
    self.assertIsNone(user)

  def tearDown(self):
    db.drop_all()

if __name__ == '__main__':
  unittest.main(verbosity=2)
