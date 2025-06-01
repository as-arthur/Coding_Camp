import pandas as pd

def transform_to_DataFrame(data):
    """Mengubah data menjadi DataFrame."""
    df = pd.DataFrame(data)
    return df

def transform_data(data, exchange_rate=16000):
    """Transformasi data dengan hasil akhir di kolom 'price' dalam Rupiah."""

    # Hapus baris dengan product_name tidak valid
    data = data[data['product_name'].str.lower() != 'unknown product']

    # Hapus simbol dolar dan konversi ke float
    data = data[data['price'].notnull()].copy()  
    data.loc[:, 'price'] = data['price'].str.replace(r'\$', '', regex=True)
    data.loc[:, 'price'] = pd.to_numeric(data['price'], errors='coerce')


    # Hapus baris yang gagal dikonversi
    data = data.dropna(subset=['price'])

    # Konversi USD ke Rupiah langsung di kolom 'price'
    data['price'] = (data['price'] * exchange_rate).astype(int)

    # Hapus duplikat dan nilai null
    data = data.drop_duplicates()
    data = data.dropna()

    # Pastikan tipe data string untuk kolom kategorikal
    data['product_name'] = data['product_name'].astype('string')
    data['size'] = data['size'].astype('string')
    data['color'] = data['color'].astype('string')
    data['gender'] = data['gender'].astype('string')

    return data
