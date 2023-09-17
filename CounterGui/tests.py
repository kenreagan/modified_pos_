import unittest
# import datetime
from utils import OrderAbc, OrderQueue 

class TestApplication(unittest.TestCase):
    def setUp(self) -> None:
        self.order0 = OrderAbc("234", "Customer0", 'barry', 'Table0', 20.00, '07947964734')
        self.order1 = OrderAbc('2225', "Customer1", 'Rigo', 'Table1', 100.0, "078378736")
        self.order2 = OrderAbc('243', "Customer2", 'jude', 'Table2', 50.0, "0753734887456")
        self.order3 = OrderAbc('3436', "Customer3", 'ivan', 'Table3', 75.0, "07637383389")
        self.queue = OrderQueue()

    def tearDown(self) -> None:
        pass

    def testOrderCreation(self):
        self.queue.add_order(self.order0)
        self.queue.add_order(self.order1)
        self.queue.add_order(self.order2)
        self.queue.add_order(self.order3)
        self.assertFalse(self.queue.is_empty())

    def testFindOrderByPhone(self):
        self.queue.add_order(self.order0)
        self.queue.add_order(self.order1)
        self.queue.add_order(self.order2)
        self.queue.add_order(self.order3)

        found_order = self.queue.find_order("07947964734")
        self.assertIsNotNone(found_order)
        self.assertEqual(found_order[0].customer_name, "Customer0")

    def testFindNonExistentOrder(self):
        self.queue.add_order(self.order1)
        self.queue.add_order(self.order2)

        found_order = self.queue.find_order("789")
        self.assertEqual(len(found_order), 0)  

if __name__ == "__main__":
    unittest.main()

