import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
import numpy as np

from main import stat

todt = lambda x: pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S')


class TestStringMethods(unittest.TestCase):
    def test_base(self):
        orders = pd.DataFrame([
            [1, 11, todt('2019-07-01 05:02:59')],
            [2, 12, todt('2019-07-02 05:02:59')],
            [3, 13, todt('2019-07-03 05:02:59')],
            [4, 14, todt('2019-07-04 05:02:59')],
            [5, 15, todt('2019-07-05 05:02:59')],
            [6, 16, todt('2019-07-06 05:02:59')],
            [7, 11, todt('2019-06-23 05:02:59')],
            [8, 11, todt('2015-06-23 05:02:59')],
        ],
            columns=['OrderId', 'CustomerId', 'DateTime']
        ).astype(dtype={'OrderId': 'int64', 'CustomerId': 'int64'})

        order_lines = pd.DataFrame([
            [111, 1, 10.0],
            [112, 2, 10.0],
            [113, 1, 10.0],
            [114, 5, 10.0],
            [111, 7, 10.0],
            [112, 2, 10.0],
            [111, 1, 10.0],
            [114, 6, 10.0],
            [115, 8, 10.0],
            [115, 8, 10.0],
            [115, 8, 10.0],
            [115, 8, 10.0],
            [115, 8, 10.0],
        ],
            columns=['ProductId', 'OrderId', 'Price'],
        ).astype(dtype={'ProductId': 'int64', 'OrderId': 'int64', 'Price': 'float'})

        wait_result = pd.DataFrame([
            [111, 30.0, 20.0],
            [112, 20.0, 20.0],
            [113, 10.0, 30.0],
            [114, 20.0, 10.0]],
            columns=['ProductId', 'TotalIncome', 'AverageCheck'],
        ).astype(dtype={'ProductId': 'int64',
                        'TotalIncome': 'float',
                        'AverageCheck': 'float'}).sort_values(by=['ProductId']).reset_index(drop=True).sort_index(axis=1)

        got_result = stat(orders, order_lines).sort_values(by=['ProductId']).reset_index(drop=True).sort_index(axis=1)

        assert_frame_equal(got_result, wait_result)

    def test_nan(self):
        orders = pd.DataFrame([
            [1, 11, todt('2019-07-01 05:02:59')],
            [2, 12, np.nan],
            [3, np.nan, todt('2019-07-03 05:02:59')],
            [np.nan, 14, todt('2019-07-04 05:02:59')],
            [5, 15, todt('2019-07-05 05:02:59')],
            [6, 16, todt('2019-07-06 05:02:59')],
            [7, 11, todt('2019-06-23 05:02:59')],
            [8, 11, todt('2015-06-23 05:02:59')],
        ],
            columns=['OrderId', 'CustomerId', 'DateTime']
        )

        order_lines = pd.DataFrame([
            [111, 1, np.nan],
            [112, 2, 10.0],
            [113, 1, 10.0],
            [114, np.nan, 10.0],
            [111, 7, 10.0],
            [112, 2, 10.0],
            [111, 1, 10.0],
            [114, 6, 10.0],
            [np.nan, 8, 10.0],
            [115, 8, 10.0],
            [115, 8, 10.0],
            [115, 8, 10.0],
            [115, 8, 10.0],
        ],
            columns=['ProductId', 'OrderId', 'Price'],
        )

        wait_result = pd.DataFrame([
            [111, 20.0, 15.0],
            [113, 10.0, 20.0],
            [114, 20.0, 10.0]],
            columns=['ProductId', 'TotalIncome', 'AverageCheck'],
        ).sort_values(by=['ProductId']).reset_index(drop=True).sort_index(axis=1)

        got_result = stat(orders, order_lines).sort_values(by=['ProductId']).reset_index(drop=True).sort_index(axis=1)

        assert_frame_equal(got_result, wait_result)

    def test_no_corr(self):
        orders = pd.DataFrame([
            [1, 11, todt('2019-07-01 05:02:59')],
            [2, 12, todt('2019-07-02 05:02:59')],
            [3, 13, todt('2019-07-03 05:02:59')],
            [4, 14, todt('2019-07-04 05:02:59')],
            [5, 15, todt('2019-07-05 05:02:59')],
            [6, 16, todt('2019-07-06 05:02:59')],
            [7, 11, todt('2019-06-23 05:02:59')],
            [8, 11, todt('2015-06-23 05:02:59')],
        ],
            columns=['OrderId', 'CustomerId', 'DateTime']
        ).astype(dtype={'OrderId': 'int64', 'CustomerId': 'int64'})

        order_lines = pd.DataFrame([
            [111, 9, 10.0],
            [112, 10, 10.0],
            [113, 11, 10.0],
            [114, 12, 10.0],
        ],
            columns=['ProductId', 'OrderId', 'Price'],
        ).astype(dtype={'ProductId': 'int64', 'OrderId': 'int64', 'Price': 'float'})

        wait_result = pd.DataFrame([],
            columns=['ProductId', 'TotalIncome', 'AverageCheck'],
        ).astype(dtype={'ProductId': 'int64',
                        'TotalIncome': 'float',
                        'AverageCheck': 'float'}).sort_values(by=['ProductId']).reset_index(drop=True).sort_index(axis=1)

        got_result = stat(orders, order_lines).sort_values(by=['ProductId']).reset_index(drop=True).sort_index(axis=1)

        assert_frame_equal(got_result, wait_result)


if __name__ == '__main__':
    unittest.main()
