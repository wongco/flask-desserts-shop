from unittest import TestCase
from desserts import Dessert, DessertList


class DessertListTests(TestCase):
    def setUp(self):
        self.sample_list = DessertList()

    def test_init(self):
        """Test the __init__ method for DessertList"""
        self.assertEqual(self.sample_list.desserts, [])
        self.assertEqual(self.sample_list.next_id, 1)

    def test_repr(self):
        """Test the __repr__ method for DessertList"""
        self.sample_list.add("Chocolate chip cookie",
                             "C is for cookie, that's good enough for me", 20)
        self.assertIn(f'id', repr(self.sample_list))
        self.assertIn(f'name', repr(self.sample_list))
        self.assertIn(f'calories', repr(self.sample_list))

    def test_add(self):
        """Test the add method for DessertList"""
        self.sample_list.add("Chocolate chip cookie",
                             "C is for cookie, that's good enough for me", 20)
        self.assertEqual(1, self.sample_list.desserts[0].id)
        self.assertEqual("Chocolate chip cookie",
                         self.sample_list.desserts[0].name)
        self.assertEqual("C is for cookie, that's good enough for me",
                         self.sample_list.desserts[0].description)
        self.assertEqual(20, self.sample_list.desserts[0].calories)
        self.assertEqual(2, self.sample_list.next_id)

    def test_serialize(self):
        """Test the serialize method for DessertList"""
        self.assertIsInstance(self.sample_list.serialize(), list)
        #  check content of list of dicts
        self.sample_list.add("Chocolate chip cookie",
                             "C is for cookie, that's good enough for me", 20)
        self.assertEqual(self.sample_list.serialize()[
                         0]['id'], self.sample_list.desserts[0].id)
        self.assertEqual(self.sample_list.serialize()[
                         0]['name'], self.sample_list.desserts[0].name)
        self.assertEqual(self.sample_list.serialize()[
                         0]['description'], self.sample_list.desserts[0].description)
        self.assertEqual(self.sample_list.serialize()[
                         0]['calories'], self.sample_list.desserts[0].calories)
