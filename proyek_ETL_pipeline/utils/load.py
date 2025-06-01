import pandas as pd
import os

def load_to_csv(dataframe, filename='products.csv'):
    """Simpan DataFrame ke file CSV lokal."""
    try:
        dataframe.to_csv(filename, index=False)
        print(f"data berhasil disimpan ke file CSV: {filename}")
        return True
    except Exception as e:
        print(f"gagal menyimpan ke CSV: {e}")
        return False

def load_to_google_sheets(dataframe, spreadsheet_name, worksheet_name, service_account_json):
    """Simpan DataFrame ke Google Sheets."""
    try:
        import gspread
        from gspread_dataframe import set_with_dataframe
        from google.oauth2.service_account import Credentials

        # Validasi file service account
        if not os.path.exists(service_account_json):
            raise FileNotFoundError(f"File service account tidak ditemukan: {service_account_json}")

        scopes = ["https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/drive"]

        credentials = Credentials.from_service_account_file(
            service_account_json, scopes=scopes)

        client = gspread.authorize(credentials)

        try:
            spreadsheet = client.open(spreadsheet_name)
        except gspread.SpreadsheetNotFound:
            spreadsheet = client.create(spreadsheet_name)
            print(f"spreadsheet baru dibuat: {spreadsheet_name}")
            # Opsional: atur permissions agar "Anyone with the link" bisa edit
            spreadsheet.share(None, perm_type='anyone', role='writer')

        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
            worksheet.clear()
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=20)

        set_with_dataframe(worksheet, dataframe)
        print(f"berhasil disimpan ke Google Sheets: {spreadsheet_name} → {worksheet_name}")
        return True
    except Exception as e:
        print(f"gagal menyimpan ke Google Sheets: {e}")
        return False

def load_to_postgresql(dataframe, table_name, db_uri):
    """Simpan DataFrame ke tabel PostgreSQL."""
    try:
        from sqlalchemy import create_engine

        engine = create_engine(db_uri)
        dataframe.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"berhasil disimpan ke PostgreSQL, tabel: {table_name}")
        return True
    except Exception as e:
        print(f"gagal menyimpan ke PostgreSQL: {e}")
        return False

def load_data(dataframe, destination, **kwargs):
    """
    Fungsi utama untuk memuat data ke tujuan yang ditentukan.
    
    destination: 'csv', 'google_sheets', atau 'postgresql'
    kwargs:
        - filename
        - spreadsheet_name, worksheet_name, service_account_json
        - table_name, db_uri
    """
    if dataframe is None or dataframe.empty:
        print("DataFrame kosong atau None")
        return False

    if destination == 'csv':
        return load_to_csv(dataframe, kwargs.get('filename', 'output.csv'))

    elif destination == 'google_sheets':
        required_params = ['spreadsheet_name', 'service_account_json']
        for param in required_params:
            if param not in kwargs:
                print(f"Parameter wajib '{param}' tidak ditemukan untuk Google Sheets")
                return False
        
        return load_to_google_sheets(
            dataframe,
            spreadsheet_name=kwargs['spreadsheet_name'],
            worksheet_name=kwargs.get('worksheet_name', 'Sheet1'),
            service_account_json=kwargs['service_account_json']
        )

    elif destination == 'postgresql':
        required_params = ['table_name', 'db_uri']
        for param in required_params:
            if param not in kwargs:
                print(f"Parameter wajib '{param}' tidak ditemukan untuk PostgreSQL")
                return False
        
        return load_to_postgresql(
            dataframe,
            table_name=kwargs['table_name'],
            db_uri=kwargs['db_uri']
        )

    else:
        print("penyimpanan tidak dikenali. Gunakan 'csv', 'google_sheets', atau 'postgresql'.")
        return False

# Alias untuk konsistensi
load = load_data