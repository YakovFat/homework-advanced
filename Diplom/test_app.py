import unittest
from user import User


class ClassVkinder(unittest.TestCase):
    def setUp(self):
        self.user = User('andreitsivenkov')

    def test_sex_user(self):
        sex = self.user.sex_user()
        user_2 = User('mariezalm')
        sex_2 = user_2.sex_user()
        self.assertEqual(sex, 1)
        self.assertEqual(sex_2, 2)

    def test_user_search(self):
        user = self.user
        self.assertIsNotNone(user.user_search())


if __name__ == "__main__":
    unittest.main()
