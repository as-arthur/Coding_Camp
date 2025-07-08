import unittest
import pandas as pd
from utils.transform import transform_to_DataFrame, transform_data 

class TestTransformFunctions(unittest.TestCase):

    def setUp(self):
        self.raw_data = [
            {
                'product_name': 'Cool Shirt',
                'price': '$10',
                'rating': '⭐ 4.5 / 5',
                'color': '3 Colors',
                'size': 'L',
                'gender': 'Unisex',
                'timestamp': '2025-06-01-12:00:00'
            },
            {
                'product_name': 'Unknown Product',
                'price': '$15',
                'rating': '⭐ 4.0 / 5',
                'color': '2 Colors',
                'size': 'M',
                'gender': 'Unisex',
                'timestamp': '2025-06-01-12:05:00'
            },
            {
                'product_name': 'Fancy Pants',
                'price': '$20',
                'rating': 'Invalid Rating',
                'color': '4 Colors',
                'size': 'S',
                'gender': 'Unisex',
                'timestamp': '2025-06-01-12:10:00'
            },
            {
                'product_name': 'Nice Hat',
                'price': None,
                'rating': '⭐ 4.0 / 5',
                'color': '1 Color',
                'size': 'One Size',
                'gender': 'Unisex',
                'timestamp': 'invalid-timestamp'
            }
        ]

    def test_transform_to_dataframe(self):
        df = transform_to_DataFrame(self.raw_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 4)
        self.assertIn('product_name', df.columns)

    def test_transform_data(self):
        df = transform_to_DataFrame(self.raw_data)
        transformed = transform_data(df)

        print("=== Transformed Data ===")
        print(transformed)


        # Harus hanya menyisakan 1 entri valid: "Cool Shirt"
        self.assertIsInstance(transformed, pd.DataFrame)
        self.assertEqual(len(transformed), 1)

        row = transformed.iloc[0]
        self.assertEqual(row['Title'], 'Cool Shirt')
        self.assertEqual(row['price'], 160000)  # $10 * 16000
        self.assertEqual(row['rating'], 4.5)
        self.assertEqual(row['color'], 3)

        self.assertIn('timestamp', transformed.columns)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(transformed['timestamp']))

    def test_transform_data_missing_fields(self):
        # Hilangkan kolom timestamp
        partial_df = pd.DataFrame([{
            'product_name': 'Basic Tee',
            'price': '$5',
            'rating': '⭐ 4.0 / 5',
            'color': '2 Colors',
            'size': 'M',
            'gender': 'Male'
        }])

        result = transform_data(partial_df)
        self.assertEqual(result.iloc[0]['price'], 80000)
        self.assertNotIn('timestamp', result.columns)
        self.assertEqual(result.iloc[0]['color'], 2)

if __name__ == '__main__':
    unittest.main()
