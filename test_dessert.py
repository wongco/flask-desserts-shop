from unittest import TestCase
from desserts import Dessert


class DessertTests(TestCase):
    def setUp(self):
        self.dessert = Dessert(1, "Snickerdoodle cookies", "Best name ever",
                               200)

    def test_init(self):
        """Test the __init__ method for Dessert"""

        self.assertEqual(self.dessert.id, 1)
        self.assertEqual(self.dessert.name, "Snickerdoodle cookies")
        self.assertEqual(self.dessert.description, "Best name ever")
        self.assertEqual(self.dessert.calories, 200)

    def test_repr(self):
        """Test the __repr__ method for Dessert"""

        test_result = '<Dessert id=1 name="Snickerdoodle cookies" calories=200>'
        self.assertEqual(str(self.dessert), test_result)

    def test_modify(self):
        """Test the modify method for Dessert"""

        self.dessert.modify("Cookies", "Lovely Baked", 30)
        self.assertEqual(self.dessert.name, "Cookies")
        self.assertEqual(self.dessert.description, "Lovely Baked")
        self.assertEqual(self.dessert.calories, 30)

    def test_serialize(self):
        """Test the serialize method for Dessert"""
        test_result = {
            'id': 1,
            'name': 'Snickerdoodle cookies',
            'description': "Best name ever",
            'calories': 200
        }
        self.assertEqual(self.dessert.serialize(), test_result)
