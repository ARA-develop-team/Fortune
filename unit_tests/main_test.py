import unittest
import sys

sys.path.append('./')
import main


class MyTestCase(unittest.TestCase):
    def test_build(self):
        self.assertEqual(main.main(), 0)


if __name__ == '__main__':
    unittest.main()
