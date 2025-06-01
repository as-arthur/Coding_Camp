from utils.extract import scrape
from utils.transform import transform_to_DataFrame, transform_data
from utils.load import load_data, load_to_google_sheets, load_to_postgresql

def main():
    # Step 1: Extract
    base_url = 'https://fashion-studio.dicoding.dev/page{}'
    raw_data = scrape(base_url)

    # Step 2: Transform
    df_raw = transform_to_DataFrame(raw_data)
    df_clean = transform_data(df_raw, exchange_rate=16000)

    # Step 3: Load
    load_data(df_clean, destination='csv', filename='fathur_products.csv')
    load_to_google_sheets(
        df_clean, 
        spreadsheet_name='fathur_product',
        worksheet_name='Sheet1',  
        service_account_json='path/to/google-sheets-api.json'  
    )


if __name__ == '__main__':
    main()
