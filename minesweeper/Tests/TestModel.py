import unittest
import sys
sys.path.append('../')

from model import Model
from controller import Controller

class TestModel(unittest.TestCase): 
    def setUp(self) -> None:
        self.model = Model()

    def test_set_controller(self): 
        controller = Controller(self.model)
        self.model.set_controller(controller)
        self.assertIsInstance(self.model.controller, Controller)

    
if __name__ == '__main__': 
    unittest.main()