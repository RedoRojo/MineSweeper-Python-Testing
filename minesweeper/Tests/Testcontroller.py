import unittest
import sys
sys.path.append('../')
from model import Model
from view import View
from controller import Controller
from PyQt5.QtWidgets import QApplication
from unittest.mock import MagicMock

class TestController(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        model = Model()
        self.controller = Controller(model)

    def test_set_view_single_path(self):
        window = View(self.controller)
        self.controller.set_view(window)
        self.assertEqual(self.controller.view, window)
    
    def test_left_click_win(self):
        self.model_mock = MagicMock()
        self.model_mock.game_status.return_value = "Win"
        self.view_mock = MagicMock()
        self.view_mock.top_box = MagicMock()
        self.view_mock.top_box.top_panel = MagicMock()
        self.view_mock.top_box.top_panel.start_btn = MagicMock()
        self.controller = Controller(self.model_mock)
        self.controller.set_view(self.view_mock)
        self.controller.left_click(0,0)
        self.view_mock.top_box.top_panel.start_btn.set_won.assert_called_once()
    
    def test_left_click_win(self):
        self.model_mock = MagicMock()
        self.model_mock.game_status.return_value = "Lose"
        self.view_mock = MagicMock()
        self.view_mock.top_box = MagicMock()
        self.view_mock.top_box.top_panel = MagicMock()
        self.view_mock.top_box.top_panel.start_btn = MagicMock()
        self.controller = Controller(self.model_mock)
        self.controller.set_view(self.view_mock)
        self.controller.left_click(0,0)
        self.view_mock.top_box.top_panel.start_btn.set_lost.assert_called_once()
    
    def test_right_click(self): 
        self.model_mock = MagicMock()
        self.view_mock = MagicMock()
        self.view_mock.top_box = MagicMock()
        self.view_mock.top_box.top_panel = MagicMock()
        self.view_mock.top_box.top_panel.start_btn = MagicMock()
        self.controller = Controller(self.model_mock)
        self.controller.set_view(self.view_mock)
        self.controller.right_click(1,1)
        self.view_mock.top_box.top_panel.board.set.assert_called_once()

    def test_start_new_game(self): 
        self.model_mock = MagicMock()
        self.view_mock = MagicMock()
        self.controller = Controller(self.model_mock)
        self.controller.set_view(self.view_mock)
        self.controller.start_new_game(); 
        self.model_mock.new_game.assert_called_once()
        self.view_mock.update.assert_called_once()
    
    def test_start_new_game_smile(self): 
        self.model_mock = MagicMock()
        self.view_mock = MagicMock()
        self.controller = Controller(self.model_mock)
        self.controller.set_view(self.view_mock)
        self.controller.start_new_game_smile(); 
        self.model_mock.new_game.assert_called_once()
        self.view_mock.update.assert_called_once()

    def test_start_new_game_easy(self): 
        self.model_mock = MagicMock()
        self.view_mock = MagicMock()
        self.controller = Controller(self.model_mock)
        self.controller.set_view(self.view_mock)
        self.controller.start_new_game_easy(); 
        self.model_mock.new_game.assert_called_once()
        self.view_mock.update.assert_called_once()

    def test_start_new_game_mid(self): 
        self.model_mock = MagicMock()
        self.view_mock = MagicMock()
        self.controller = Controller(self.model_mock)
        self.controller.set_view(self.view_mock)
        self.controller.start_new_game_mid(); 
        self.model_mock.new_game.assert_called_once()
        self.view_mock.update.assert_called_once()


if __name__ == '__main__':
    unittest.main()