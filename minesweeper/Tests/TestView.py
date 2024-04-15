import unittest
import unittest
import sys
sys.path.append('../')
from unittest.mock import MagicMock
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel
from unittest.mock import patch


from view import View
from view import StartButton
from view import Board

class TestView(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.mock_controller = MagicMock()
        self.mock_controller.get_mines_max.return_value = 10
        self.view = View(self.mock_controller)

    def test_createMainUI(self):
        self.mock_controller.get_field_width.return_value = 10
        self.mock_controller.get_field_height.return_value = 8
        self.view.createMainUI()
        self.assertEqual(self.view.width(), 340)  
        self.assertEqual(self.view.height(), 346)
        self.assertEqual(self.view.windowTitle(), "Minesweeper")
        self.assertTrue(self.view.centralWidget().layout() is not None)
        self.assertEqual(self.view.centralWidget().layout(), self.view.top_box)
        self.assertEqual(self.view.top_box.alignment(), Qt.AlignCenter)
    
    @patch('PyQt5.QtWidgets.QInputDialog.getText', return_value=("User Input", True))
    def test_input_box_text_success(self, input_mock):
        result = self.view.input_box_text("Title", "Info")
        self.assertEqual(result, "User Input")

    @patch('PyQt5.QtWidgets.QInputDialog.getText', return_value=(None, False))
    def test_input_box_text_cancel(self, input_mock):
        with self.assertRaises(SystemExit):
            self.view.input_box_text("Title", "Info")


    @patch('PyQt5.QtWidgets.QInputDialog.getInt', return_value=("6", True))
    def test_input_box_int_success(self, input_mock):
        result = self.view.input_box_int("Title", "Info")
        self.assertEqual(result, "6")

    @patch('PyQt5.QtWidgets.QInputDialog.getInt', return_value=(None, False))
    def test_input_box_int_cancel(self, input_mock):
        with self.assertRaises(SystemExit):
            self.view.input_box_int("Title", "Info")        

class TestStartButton(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.controller_mock = MagicMock()
        self.start_button = StartButton(self.controller_mock)
    
    def test_load_smiles_success(self):
        QPixmap.return_value = QPixmap(44, 44)
        self.start_button.load_smiles()
        self.assertIsNotNone(self.start_button.smiles)
        self.assertEqual(len(self.start_button.smiles), 4)
        for pixmap in self.start_button.smiles:
            self.assertIsInstance(pixmap, QPixmap)
    
    def test_mousePressEvent_left_button(self):
        event = MagicMock()
        event.button.return_value = Qt.LeftButton
        self.start_button.mousePressEvent(event)
        self.controller_mock.start_new_game_smile.assert_called_once()
        self.assertIsNotNone(self.start_button.pixmap())
    
    def test_mousePressEvent_other_button(self):
        event = MagicMock()
        event.button.return_value = Qt.RightButton
        self.start_button.mousePressEvent(event)
        self.controller_mock.start_new_game_smile.assert_not_called()

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.board = Board()
    
    def test_init_board_non_empty_number(self):
        numbers = 3
        self.board.init_board(numbers)
        self.assertEqual(len(self.board.numbers), 3)
        for widget in self.board.numbers:
            self.assertIsInstance(widget, QLabel)
            self.assertIsNotNone(widget.pixmap())
    
    def test_init_board_empty_number(self):
        numbers = 0
        self.board.init_board(numbers)
        self.assertEqual(len(self.board.numbers), 0)

if __name__ == '__main__':
    unittest.main()
