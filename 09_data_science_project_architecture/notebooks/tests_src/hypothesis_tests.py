import unittest
import pandas as pd
from hypothesis import given, strategies as st
from hypothesis import settings
from hypothesis import assume
from notebooks.func.data_main_structure import column_mapping, get_columns


@st.composite
def simple_dfs(draw):
    n_cols = draw(st.integers(min_value=1, max_value=6))
    n_rows = draw(st.integers(min_value=0, max_value=8))
    col_names = draw(st.lists(st.text(min_size=1), min_size=n_cols, max_size=n_cols, unique=True))
    data = {}
    for name in col_names:
        data[name] = draw(st.lists(st.integers(min_value=-10 ** 6, max_value=10 ** 6),
                                   min_size=n_rows, max_size=n_rows))
    return pd.DataFrame(data)


@st.composite
def df_and_valid_indices(draw):
    df = draw(simple_dfs())
    n = df.shape[1]
    idxs = draw(st.lists(st.integers(min_value=-n, max_value=n - 1),
                         min_size=1, max_size=n, unique=False))
    assume(any((-n <= i <= n - 1) for i in idxs))
    return df, idxs


@st.composite
def df_and_invalid_index(draw):
    df = draw(simple_dfs())
    n = df.shape[1]
    bad = draw(st.integers().filter(lambda i: i >= n or i < -n))
    return df, bad


class TestColumnMapping(unittest.TestCase):

    def test_basic(self):
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4], 'C': [5, 6]})
        m = column_mapping(df)
        self.assertEqual(list(m.keys()), list(range(df.shape[1])))
        self.assertEqual(list(m.values()), list(df.columns))

    def test_empty_df(self):
        df = pd.DataFrame()
        m = column_mapping(df)
        self.assertEqual(m, {})

    def test_duplicate_colnames(self):
        df = pd.DataFrame([[1, 2, 3]], columns=['A', 'A', 'B'])
        m = column_mapping(df)
        self.assertEqual(list(m.keys()), [0, 1, 2])
        self.assertEqual(list(m.values()), ['A', 'A', 'B'])

    @settings(deadline=None, max_examples=200)
    @given(df=simple_dfs())
    def test_property_matches_enumerate(self, df):
        m = column_mapping(df)
        self.assertEqual(list(m.items()), list(enumerate(df.columns)))


class TestGetColumns(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame(
            {
                'A': [1, 2, 3],
                'B': [4, 5, 6],
                'C': [7, 8, 9],
                'D': [10, 11, 12],
                'E': [13, 14, 15],
                'F': [16, 17, 18],
            }
        )

    def test_select_some(self):
        res = get_columns(self.df, 0, 2)
        exp = self.df[['A', 'C']]
        pd.testing.assert_frame_equal(res, exp)

    def test_allows_duplicates(self):
        res = get_columns(self.df, 1, 1)
        exp = self.df.iloc[:, [1, 1]]
        pd.testing.assert_frame_equal(res, exp)

    def test_negative_indices(self):
        res = get_columns(self.df, -1, -3)
        exp = self.df.iloc[:, [-1, -3]]
        pd.testing.assert_frame_equal(res, exp)

    def test_invalid_index_raises(self):
        with self.assertRaises(IndexError):
            get_columns(self.df, 999)

    @settings(deadline=None, max_examples=200)
    @given(data=df_and_valid_indices())
    def test_property_equivalent_to_iloc(self, data):
        df, idxs = data
        res = get_columns(df, *idxs)
        exp = df.iloc[:, list(idxs)]
        pd.testing.assert_frame_equal(res, exp)

    @settings(deadline=None, max_examples=50)
    @given(data=df_and_invalid_index())
    def test_property_invalid_indices_raise(self, data):
        df, bad = data
        with self.assertRaises(IndexError):
            get_columns(df, bad)


if __name__ == "__main__":
    unittest.main()
