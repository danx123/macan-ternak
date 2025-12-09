#`tests/test_tiger_pet.py`

import unittest
from logic.tiger_pet import TigerPet

class TestTigerPet(unittest.TestCase):
    def setUp(self):
        self.pet = TigerPet()
    
    def test_initial_stats(self):
        self.assertEqual(self.pet.hunger, 100)
        self.assertEqual(self.pet.energy, 100)
        self.assertEqual(self.pet.level, 1)
    
    def test_hunger_decay(self):
        initial_hunger = self.pet.hunger
        self.pet.update(1.0)
        self.assertLess(self.pet.hunger, initial_hunger)
    
    def test_feeding(self):
        self.pet.hunger = 50
        success, _ = self.pet.feed()
        self.assertTrue(success)
        self.assertEqual(self.pet.hunger, 90)
    
    def test_feeding_when_full(self):
        self.pet.hunger = 95
        success, _ = self.pet.feed()
        self.assertFalse(success)
    
    def test_leveling_up(self):
        self.pet.exp = 0
        self.pet.add_exp(100)
        self.assertEqual(self.pet.level, 2)
        self.assertLess(self.pet.exp, 100)

if __name__ == '__main__':
    unittest.main()