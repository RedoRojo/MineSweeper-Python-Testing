import unittest
import sys
sys.path.append('../')

from cell import Cell

class TestCell(unittest.TestCase):
    def setUp(self):
        self.cell = Cell(0,0)

    def test_open_cell_flagged(self): 
        self.cell.state = "flagged"
        self.cell.open()
        self.assertEqual(self.cell.state, "flagged"); 
    
    def test_next_mark(self):
        self.cell.state = "flagged"
        self.cell.next_mark()
        self.assertEqual(self.cell.state, "questioned")
        self.assertEqual(self.cell.int_state, 11)

if __name__ == '__main__':
    unittest.main()