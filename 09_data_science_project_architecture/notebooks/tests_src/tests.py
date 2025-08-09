import unittest
import pandas as pd
from notebooks.func.data_main_structure import *


class TestColumnMapping(unittest.TestCase):
    def test_column_mapping_basic(self):
        df = pd.DataFrame(
            {
                'A': [1, 2],
                'B': [3, 4],
                'C': [5, 6],
                'D': [7, 8]
            }
        )
        expected = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
        result = column_mapping(df)
        self.assertEqual(result, expected)


class TestGetColumns(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [7, 8, 9],
            'D': [10, 11, 12],
            'E': [13, 14, 15],
            'F': [16, 17, 18],
        })

    def test_get_columns_first_test(self):
        res = get_columns(self.df, 0, 2)
        exp = self.df[['A', 'C']]
        pd.testing.assert_frame_equal(res, exp)

    def test_get_columns_second_test(self):
        res = get_columns(self.df, 0, 2, 4, 5)
        exp = self.df[['A', 'C', 'E', 'F']]
        pd.testing.assert_frame_equal(res, exp)


if __name__ == '__main__':
    unittest.main()
