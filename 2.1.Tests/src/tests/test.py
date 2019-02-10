import unittest
from src.helpers.config import Config


class TestClass(unittest.TestCase):
    def setUp(self):
        self.config = Config()

    def test_1(self):
        self.con_1 = self.config.get_verbosity_level()
        self.assertIsNone(self.con_1, "Тест не выполнен")

    def test_2(self):
        self.con_2 = self.config.get_verbosity_level(level='console')
        self.assertIsNotNone(self.con_2, "Тест не выполнен")


if __name__ == '__main__':
    unittest.main()
