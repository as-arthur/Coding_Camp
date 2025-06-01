import unittest
import os
import pandas as pd
from utils.load import load_to_csv

class TestLoad(unittest.TestCase):
    def test_save_to_csv(self):
        df = pd.DataFrame({"col1": [1], "col2": ["data"]})
        filename = "tests/test_output.csv"
        load_to_csv(df, filename)
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
