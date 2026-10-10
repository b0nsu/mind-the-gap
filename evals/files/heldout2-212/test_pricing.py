import unittest

from pricing import order_total


class OrderTotalTest(unittest.TestCase):
    def test_small_order_has_no_discount(self):
        self.assertEqual(order_total(40), 40)

    def test_bulk_order_gets_discount(self):
        self.assertEqual(order_total(200), 180.0)

    def test_threshold_is_inclusive(self):
        self.assertEqual(order_total(100), 90.0)


if __name__ == "__main__":
    unittest.main()
