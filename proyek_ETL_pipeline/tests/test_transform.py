import pandas as pd
from utils.transform import transform_data

def test_transform_data_clean_and_convert():
    df = pd.DataFrame({
        'product_name': ['Shirt', 'unknown product', 'Shoes'],
        'price': ['$100.0', '$150.0', '$50.0'],
        'size': ['M', 'L', '42'],
        'color': ['Blue', 'Red', 'Black'],
        'gender': ['Male', 'Female', 'Unisex']
    })

    result = transform_data(df, exchange_rate=16000)

    assert result.shape[0] == 2  # 'unknown product' harus dibuang
    assert result['price'].iloc[0] == 100.0 * 16000
