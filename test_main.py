import unittest

class TestFunctions(unittest.TestCase):
    def test_total(self):
        result = total(3, 5)
        self.assertEqual(result, 8)

        result = total(-2, 7)
        self.assertEqual(result, 5)

        result = total(0, 0)
        self.assertEqual(result, 0)

    def test_divide(self):
        result = divide(10, 2)
        self.assertEqual(result, 5)

        result = divide(8, 4)
        self.assertEqual(result, 2)

        result = divide(5, 0)
        self.assertEqual(result, "You can't divide by zero")

if __name__ == '__main__':
    unittest.main()