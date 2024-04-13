import unittest
import sys
sys.path.append('../')

from model import Model
from controller import Controller

class TestModel(unittest.TestCase): 
    def setUp(self) -> None:
        self.model = Model()
        self.model.FIELD_WIDTH = 100

    def test_set_controller(self): 
        controller = Controller(self.model)
        self.model.set_controller(controller)
        self.assertIsInstance(self.model.controller, Controller)

    def test_get_field_width(self): 
        self.assertEqual(self.model.get_FIELD_WIDTH(), 100)

    def test_get_field_height(self): 
        self.model.FIELD_HEIGHT = 100
        self.assertEqual(self.model.get_FIELD_HEIGHT(), 100)

    
if __name__ == '__main__': 
    unittest.main()