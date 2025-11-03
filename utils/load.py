import pandas as pd
import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)

def load_data_csv(df, filename="products.csv"):
    if df.empty:
        print("Data kosong")
        return
    try:
        df.to_csv(filename, index=False)
        print(f"Data disimpan di {filename}")
        print(f"Total baris : {len(df)}")
    except Exception as e:
        print(f"Error menyimpan data ke CSV: {e}")
        raise

def load_to_postgres(df, table_name="products"):
    from sqlalchemy import create_engine
    config = {
        "database": "fashion_studio",
        "user": "postgres",
        "password": "password",
        "host": "localhost",
        "port": "5432"
    }
    db_uri = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
        
    try:
        engine = create_engine(db_uri)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print("Data loaded to PostgreSQL")
    except Exception as e:
        print(f"Error PostgreSQL: {e}")

def load_to_gdrive(df: pd.DataFrame, spreadsheet_id: str, creds_path: str):
    try:
        creds = Credentials.from_service_account_file(creds_path) 
        service = build('sheets', 'v4', credentials=creds) 
        sheet = service.spreadsheets() 

        values = [df.columns.tolist()] + df.values.tolist()
        body = {'values': values}
        
        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A1",
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print("Data disimpan ke Google Sheets.")
    
    except Exception as e:
        print(f"Error Google Sheets: {e}")

def load_to_csv(df: pd.DataFrame, filename: str):
    try:
        df.to_csv(filename, index=False)
        print(f"Data loaded to {filename}")
    except Exception as e:
        print(f"Error load data to CSV: {e}")