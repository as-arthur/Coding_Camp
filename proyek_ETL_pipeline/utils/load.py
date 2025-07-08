import pandas as pd
import os

def load_to_csv(dataframe, filename='fathur_products.csv'):
    """Simpan DataFrame ke file CSV lokal."""
    try:
        dataframe.to_csv(filename, index=False)
        print(f"data berhasil disimpan ke file CSV: {filename}")
        return True
    except Exception as e:
        print(f"gagal menyimpan ke CSV: {e}")
        return False

