from utils.extract import scrape
from utils.transform import transform_to_DataFrame, transform_data
from utils.load import load_to_csv

def main():
    # Step 1: Extract
    base_url = 'https://fashion-studio.dicoding.dev/page{}'
    raw_data = scrape(base_url)

    # Step 2: Transform
    df_raw = transform_to_DataFrame(raw_data)
    df_clean = transform_data(df_raw, exchange_rate=16000)

    # Step 3: Load
    load_to_csv(df_clean, filename='fathur_products.csv')


if __name__ == '__main__':
    main()
