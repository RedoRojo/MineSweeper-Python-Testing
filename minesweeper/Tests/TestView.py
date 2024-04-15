import unittest
import unittest
import sys
sys.path.append('../')
from unittest.mock import MagicMock
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from unittest.mock import patch


from view import View
from view import StartButton

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
        self.controller = MagicMock()
        self.start_button = StartButton(self.controller)
    
    def test_load_smiles_success(self):
        QPixmap.return_value = QPixmap(44, 44)
        self.start_button.load_smiles()
        self.assertIsNotNone(self.start_button.smiles)
        self.assertEqual(len(self.start_button.smiles), 4)
        for pixmap in self.start_button.smiles:
            self.assertIsInstance(pixmap, QPixmap)


if __name__ == '__main__':
    unittest.main()
