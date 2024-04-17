import unittest
import sys
sys.path.append('../')
from unittest import mock
from unittest.mock import MagicMock
from PyQt5.QtGui import QPixmap, QMouseEvent, QPaintEvent, QPainter
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QLabel, QMenuBar
from PyQt5.QtTest import QTest
from unittest.mock import patch


from view import View
from view import StartButton
from view import Board
from view import Field

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
    
    def test_create_menu_bar(self):
        self.view.create_menubar()
        self.assertIsInstance(self.view.menubar, QMenuBar)
        self.assertIsNotNone(self.view.gamemenu)
        self.assertEqual(self.view.gamemenu.title(), "&Game")
        self.assertIsNotNone(self.view.savemenu)
        self.assertEqual(self.view.savemenu.title(), "&Save")
    
    def test_create_top_box(self):
        self.view.create_top_box()
        self.assertIsNotNone(self.view.top_box)
    
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

    def test_load_digits_happy_path(self):
        self.board.load_digits()
        self.assertEqual(len(self.board.digits), 11) ## preguntar al mgr
    
    def test_load_digits_number_range_is_zero(self):
        with patch.object(__builtins__, 'range', return_value=range(0)):
            self.board.load_digits()
            self.assertEqual(len(self.board.digits), 0)
    
    def test_set_board_first_path(self):
        number = 10
        self.board.numbers = []
        self.assertEqual(self.board.set(number), False)

    def test_set_second_path(self):
        number = -10
        self.board.numbers = [MagicMock(), MagicMock()]
        self.board.set(number)
        self.assertEqual(self.board.k, 2)
    
    def test_set_third_path(self):
        number = 1
        self.board.numbers = [MagicMock() for _ in range(3)]
        self.board.set(number)
        self.assertEqual(self.board.out_of_boundary, True)
    
class TestField(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()
        self.field = Field(self.controller_mock, self.top_panel_mock)

    def test_load_assets(self):
        self.field.load_assets()
        self.assertIsInstance(self.field.assets, list)
        self.assertTrue(len(self.field.assets) > 0)
        for i in range(9):
            self.assertIsInstance(self.field.assets[i], QPixmap)

        files = [
            "blank",
            "flagged",
            "question",
            "mine",
            "mineclicked",
            "misflagged",
        ]

        for i, file in enumerate(files, start=9):
            self.assertIsInstance(self.field.assets[i], QPixmap)
    
    def test_mouse_release_event_first_path(self):
        event_mock = MagicMock()
        event_mock.pos.return_value = QPoint(-100,-100)
        with patch.object(self.field, 'update') as update_mock:
            self.field.mouseReleaseEvent(event_mock)
        value = self.field.out_of_frame
        self.assertEqual(value, True)
    
    def test_mouse_release_event_second_path(self):
        event_mock = MagicMock(spec=QMouseEvent)
        event_mock.pos.return_value = QPoint(1, 1)
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()
        self.controller_mock.get_status.return_value = "Win"
        self.controller_mock.get_field_width.return_value = 100
        self.controller_mock.get_field_height.return_value = 100
        self.field = Field(self.controller_mock, self.top_panel_mock)
        self.field.mouseReleaseEvent(event_mock)
        self.assertEqual(self.field.is_winner, True)
    
    def test_mouse_release_event_third_path(self):
        event_mock = MagicMock(spec=QMouseEvent)
        event_mock.pos.return_value = QPoint(1, 1)
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()
        self.controller_mock.get_status.return_value = "Lose"
        self.controller_mock.get_field_width.return_value = 100
        self.controller_mock.get_field_height.return_value = 100
        self.field = Field(self.controller_mock, self.top_panel_mock)
        self.field.mouseReleaseEvent(event_mock)
        self.assertEqual(self.field.is_winner, False)

    def test_mouse_release_event_fourth_path(self):
        event_mock = MagicMock(spec=QMouseEvent)
        event_mock.pos.return_value = QPoint(1, 1)
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()
        self.controller_mock.get_status.return_value = "Game"
        self.controller_mock.get_field_width.return_value = 100
        self.controller_mock.get_field_height.return_value = 100

        mock_field = [[MagicMock() for _ in range(100)] for _ in range(100)]
        self.controller_mock.get_field.return_value = mock_field

        self.field = Field(self.controller_mock, self.top_panel_mock)
        self.field.last_x = 10
        self.field.last_y = 10
        self.field.mouseReleaseEvent(event_mock)
        self.assertEqual(self.field.distinct_coords, True)
    
    def test_mouse_release_event_fifth_path(self):
        event_mock = MagicMock(spec=QMouseEvent)
        event_mock.pos.return_value = QPoint(1, 1)
        event_mock.button.return_value = Qt.LeftButton
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()
        self.controller_mock.get_status.return_value = "Game"
        self.controller_mock.get_field_width.return_value = 100
        self.controller_mock.get_field_height.return_value = 100
        self.field = Field(self.controller_mock, self.top_panel_mock)
        self.field.last_x = 0
        self.field.last_y = 0
        self.field.mouseReleaseEvent(event_mock)
        self.controller_mock.left_click.assert_called_once
    
    def test_mouse_release_event_fifth_path(self):
        event_mock = MagicMock(spec=QMouseEvent)
        event_mock.pos.return_value = QPoint(1, 1)
        event_mock.button.return_value = Qt.RightButton
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()
        self.controller_mock.get_status.return_value = "Game"
        self.controller_mock.get_field_width.return_value = 100
        self.controller_mock.get_field_height.return_value = 100
        self.field = Field(self.controller_mock, self.top_panel_mock)
        self.field.last_x = 0
        self.field.last_y = 0
        self.field.mouseReleaseEvent(event_mock)
        self.controller_mock.right_click.assert_called_once
    
    def test_mouse_press_event_first_path(self):
        event_mock = MagicMock(spec=QMouseEvent)
        event_mock.pos.return_value = QPoint(1, 1)
        event_mock.button.return_value = Qt.RightButton
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()

        field_mock = [[MagicMock() for _ in range(100)] for _ in range(100)]
        field_mock[0][0].int_state = 9 

        self.controller_mock.get_status.return_value = "Game"
        self.controller_mock.get_field_width.return_value = 100
        self.controller_mock.get_field_height.return_value = 100
        self.controller_mock.get_field.return_value = field_mock
        
        self.field = Field(self.controller_mock, self.top_panel_mock)
        self.field.mousePressEvent(event_mock)
        self.assertEqual(self.field.distinct_coords, True)
    
    def test_mouse_press_event_second_path(self):
        event_mock = MagicMock(spec=QMouseEvent)
        event_mock.pos.return_value = QPoint(-1, -1)
        event_mock.button.return_value = Qt.RightButton
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()

        self.controller_mock.get_field_width.return_value = 100
        self.controller_mock.get_field_height.return_value = 100
        
        self.field = Field(self.controller_mock, self.top_panel_mock)
        self.field.mousePressEvent(event_mock)
        self.assertEqual(self.field.out_of_frame, True)
    
    def test_mouse_press_event_third_path(self):
        event_mock = MagicMock(spec=QMouseEvent)
        event_mock.pos.return_value = QPoint(1, 1)
        event_mock.button.return_value = Qt.LeftButton
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()

        field_mock = [[MagicMock() for _ in range(100)] for _ in range(100)]
        field_mock[0][0].int_state = 9 

        self.controller_mock.get_status.return_value = "Game"
        self.controller_mock.get_field_width.return_value = 100
        self.controller_mock.get_field_height.return_value = 100
        self.controller_mock.get_field.return_value = field_mock
        
        self.field = Field(self.controller_mock, self.top_panel_mock)
        self.field.mousePressEvent(event_mock)
        self.assertEqual(self.field.controller.get_field()[0][0].int_state, 0)
    
    def test_mouse_press_event_fourth_path(self):
        event_mock = MagicMock(spec=QMouseEvent)
        event_mock.pos.return_value = QPoint(1, 1)
        event_mock.button.return_value = Qt.LeftButton
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()

        field_mock = [[MagicMock() for _ in range(100)] for _ in range(100)]
        field_mock[0][0].int_state = 8 

        self.controller_mock.get_status.return_value = "Game"
        self.controller_mock.get_field_width.return_value = 100
        self.controller_mock.get_field_height.return_value = 100
        self.controller_mock.get_field.return_value = field_mock
        
        self.field = Field(self.controller_mock, self.top_panel_mock)
        self.field.mousePressEvent(event_mock)
        self.assertNotEqual(self.field.controller.get_field()[0][0].int_state, 0)
        self.assertEqual(self.field.distinct_coords, False)
    
    def test_mouse_press_event_fourth_path(self):
        event_mock = MagicMock(spec=QMouseEvent)
        event_mock.pos.return_value = QPoint(1, 1)
        event_mock.button.return_value = Qt.LeftButton
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()
        self.controller_mock.get_status.return_value = "NoGame"
        self.controller_mock.get_field_width.return_value = 100
        self.controller_mock.get_field_height.return_value = 100
        self.field = Field(self.controller_mock, self.top_panel_mock)
        self.field.last_x = 10000
        self.field.last_y = 10000
        self.field.mousePressEvent(event_mock)
        self.assertNotEqual((self.field.last_x, self.field.last_y), (0,0))
    
    def test_for_test_mouse_coordinates(self):
        event_mock = MagicMock(spec=QMouseEvent)
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()
        self.controller_mock.get_field_width.return_value = 100
        self.controller_mock.get_field_height.return_value = 100
        self.field = Field(self.controller_mock, self.top_panel_mock)
        x = 1
        y = 1
        result = self.field.test_mouse_coordinates(x,y)
        self.assertEqual(result, True)
    
    def test_for_test_mouse_coordinates_second_path(self):
        event_mock = MagicMock(spec=QMouseEvent)
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()
        self.controller_mock.get_field_width.return_value = 100
        self.controller_mock.get_field_height.return_value = 100
        self.field = Field(self.controller_mock, self.top_panel_mock)
        x = -1
        y = 1
        result = self.field.test_mouse_coordinates(x,y)
        self.assertEqual(result, False)
    
    def test_paint_event_first_path(self):
        event_mock = MagicMock(spec=QPaintEvent)
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()
        self.controller_mock.get_field_width.return_value = 2
        self.controller_mock.get_field_height.return_value = 2

        field_mock = [
            [MagicMock(int_state=0), MagicMock(int_state=1)],
            [MagicMock(int_state=2), MagicMock(int_state=3)]
        ]
        self.controller_mock.get_field.return_value = field_mock
        self.field = Field(self.controller_mock, self.top_panel_mock)
        painter_mock = MagicMock(spec=QPainter)
        with patch.object(self.field, 'painter', painter_mock):
            with patch.object(self.field.controller, 'get_field') as get_field_mock:
                self.field.paintEvent(event_mock)
        get_field_mock.assert_called()
    
    def test_paint_event_second_path(self):
        event_mock = MagicMock(spec=QPaintEvent)
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()
        self.controller_mock.get_field_width.return_value = 0
        self.controller_mock.get_field_height.return_value = 2

        field_mock = [
            [MagicMock(int_state=0), MagicMock(int_state=1)],
            [MagicMock(int_state=2), MagicMock(int_state=3)]
        ]
        self.controller_mock.get_field.return_value = field_mock
        self.field = Field(self.controller_mock, self.top_panel_mock)
        painter_mock = MagicMock(spec=QPainter)
        with patch.object(self.field, 'painter', painter_mock):
            with patch.object(self.field.controller, 'get_field') as get_field_mock:
                self.field.paintEvent(event_mock)
        get_field_mock.assert_not_called()
    
    def test_paint_event_third_path(self):
        event_mock = MagicMock(spec=QPaintEvent)
        self.controller_mock = MagicMock()
        self.top_panel_mock = MagicMock()
        self.controller_mock.get_field_width.return_value = 0
        self.controller_mock.get_field_height.return_value = 0
        self.field = Field(self.controller_mock, self.top_panel_mock)
        painter_mock = MagicMock(spec=QPainter)
        with patch.object(self.field, 'painter', painter_mock):
            with patch.object(self.field.controller, 'get_field') as get_field_mock:
                self.field.paintEvent(event_mock)
        get_field_mock.assert_not_called()

if __name__ == '__main__':
    unittest.main()
