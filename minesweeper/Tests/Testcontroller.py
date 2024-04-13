import unittest
import sys
sys.path.append('../')
from model import Model
from view import View
from controller import Controller
from PyQt5.QtWidgets import QApplication

class TestController(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        model = Model()
        self.controller = Controller(model)

    def test_set_view_single_path(self):
        window = View(self.controller)
        self.controller.set_view(window)
        self.assertEqual(self.controller.view, window)

if __name__ == '__main__':
    unittest.main()