import unittest
import os
import pandas as pd
from utils.load import load_to_csv  

class TestLoadToCSV(unittest.TestCase):
    
    def setUp(self):
        # DataFrame sederhana untuk pengujian
        self.test_df = pd.DataFrame({
            'produk': ['Kaos', 'Jaket'],
            'harga': [100000, 200000]
        })
        self.filename = 'test_output.csv'
    
    def tearDown(self):
        # Hapus file hasil tes setelah selesai
        if os.path.exists(self.filename):
            os.remove(self.filename)
    
    def test_load_to_csv_success(self):
        # Jalankan fungsi
        result = load_to_csv(self.test_df, self.filename)
        
        # Pastikan fungsi return True dan file ada
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.filename))
        
        # Baca kembali dan bandingkan isinya
        loaded_df = pd.read_csv(self.filename)
        pd.testing.assert_frame_equal(loaded_df, self.test_df)

    def test_load_to_csv_invalid_dataframe(self):
        # Coba simpan objek bukan DataFrame
        result = load_to_csv("bukan dataframe", self.filename)
        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.filename))

if __name__ == '__main__':
    unittest.main()
