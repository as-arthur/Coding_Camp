import pandas as pd

def transform_to_DataFrame(data):
    """Mengubah data menjadi DataFrame."""
    df = pd.DataFrame(data)
    return df

def transform_data(data, exchange_rate=16000):
    """Transformasi data dengan hasil akhir di kolom 'price' dalam Rupiah."""

    # Hapus baris dengan product_name tidak valid
    data = data[data['product_name'].str.lower() != 'unknown product']

    # Hapus simbol dolar dan konversi ke float (jika masih dalam format $)
    data = data[data['price'].notnull()].copy()  
    if data['price'].dtype == 'object':
        data.loc[:, 'price'] = data['price'].astype(str).str.replace(r'\$', '', regex=True)
        data.loc[:, 'price'] = pd.to_numeric(data['price'], errors='coerce')
        data = data.dropna(subset=['price'])
        # Konversi USD ke Rupiah hanya jika belum dalam Rupiah
        data['price'] = (data['price'] * exchange_rate).astype(float)

    # Hapus duplikat dan nilai null
    data = data.drop_duplicates()
    data = data.dropna()

    def clean_rating(r):
        """Membersihkan rating dari format '⭐ 3.9 / 5' menjadi float"""
        if isinstance(r, str):
            # Hapus emoji dan simbol lainnya, ambil angka sebelum '/'
            if '/' in r:
                try:
                    rating_part = r.split('/')[0]
                    import re
                    rating_clean = re.sub(r'[^\d.]', '', rating_part)
                    return float(rating_clean)
                except:
                    return None
            if r.lower() == "invalid rating":
                return None
        try:
            return float(r)
        except:
            return None

    data.loc[:, 'rating'] = data['rating'].apply(clean_rating)
    data = data.dropna(subset=['rating'])   

    def clean_color(c):
        """Ekstrak angka dari format '3 Colors' menjadi integer"""
        if isinstance(c, str):
            import re
            match = re.search(r'(\d+)', c)
            if match:
                return int(match.group(1))
        return None

    data.loc[:, 'color'] = data['color'].apply(clean_color)
    data = data.dropna(subset=['color'])

    data['product_name'] = data['product_name'].astype('string')
    data['size'] = data['size'].astype('string')
    data['gender'] = data['gender'].astype('string')
    
    if 'timestamp' in data.columns:
        data.loc[:, 'timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
        data = data.dropna(subset=['timestamp'])
        data['timestamp'] = data['timestamp'].astype('datetime64[ns]')

    data = data.drop_duplicates()
    data = data.dropna()

    desired_columns = ['product_name', 'price', 'rating', 'color', 'size', 'gender']
    if 'timestamp' in data.columns:
        desired_columns.append('timestamp')
    
    available_columns = [col for col in desired_columns if col in data.columns]
    data = data[available_columns]

    data = data.rename(columns={'product_name': 'Title'})

    return data
