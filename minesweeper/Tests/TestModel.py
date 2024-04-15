import unittest
import sys
sys.path.append('../')

from model import Model
from controller import Controller
from cell import Cell

class TestModel(unittest.TestCase): 
    def setUp(self) -> None:
        self.model = Model()
        self.model.FIELD_HEIGHT = 10
        self.model.FIELD_WIDTH = 10
        self.model.MINES_MAX = 60
        controller = Controller(self.model)
        self.model.set_controller(controller)

    def test_set_controller(self): 
        controller = Controller(self.model)
        self.model.set_controller(controller)
        self.assertIsInstance(self.model.controller, Controller)

    def test_get_field_width(self): 
        self.model.FIELD_WIDTH = 100
        self.assertEqual(self.model.get_FIELD_WIDTH(), 100)

    def test_get_field_height(self): 
        self.model.FIELD_HEIGHT = 100
        self.assertEqual(self.model.get_FIELD_HEIGHT(), 100)

    def test_get_mines_max(self): 
        self.model.MINES_MAX = 60
        self.assertEqual(self.model.get_MINES_MAX(), 60)

    def test_create_field_full_of_mines(self):
        self.model.FIELD_HEIGHT = 10
        self.model.FIELD_WIDTH = 10
        self.model.MINES_MAX = 100
        
        self.model.create_field()
        self.assertIsInstance(self.model.field, list)
        self.assertIsInstance(self.model.field[0], list)
        self.assertIsInstance(self.model.field[0][0], Cell)

    def test_create_normal_field(self): 
        self.model.FIELD_HEIGHT = 20
        self.model.FIELD_WIDTH = 10
        self.model.MINES_MAX = 100
        
        self.model.create_field()
        self.assertIsInstance(self.model.field, list)
        self.assertIsInstance(self.model.field[0], list)
        self.assertIsInstance(self.model.field[0][0], Cell)

    def test_get_field(self): 
        self.model.FIELD_HEIGHT = 10
        self.model.FIELD_WIDTH = 10
        self.model.MINES_MAX = 60
        
        self.model.create_field()
        obtained_field = self.model.get_field()
        self.assertIsInstance(obtained_field, list)
        self.assertIsInstance(obtained_field[0], list)
        self.assertIsInstance(obtained_field[0][0], Cell)
        
    def test_get_cell(self):
        self.model.FIELD_HEIGHT = 10
        self.model.FIELD_WIDTH = 10
        self.model.MINES_MAX = 60
        self.model.create_field()
        self.assertIsInstance(self.model.get_cell(1,1), Cell)

    def test_get_seconds_from_the_start(self): 
        self.assertEqual(self.model.get_seconds_from_start(), 1) 
        
    def test_new_game_without_flagged_cells(self): 
        self.model.flagged_cells = -1
        self.model.new_game()
        self.assertIsInstance(self.model.get_field(), list)
    
if __name__ == '__main__': 
    unittest.main()