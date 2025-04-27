from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

def load_to_csv(filename, df):
    """"Store data to CSV File"""
    try:
        df.to_csv(filename, index=False)
        print(f"Data successfully saved to {filename}")
    except FileNotFoundError:
        print(f"FileNotFoundError: The file path '{filename}' is invalid.")
    except PermissionError:
        print(f"PermissionError: No permission to write to '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred while saving to CSV: {e}")

def load_to_google_sheets(spreadsheet_id, df):
    """Store data into google sheets using Google Sheets API"""
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file('./google-sheets-api.json', scopes=SCOPES)

    RANGE_NAME = 'Sheet1!A1'

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheets = service.spreadsheets()

        values = [df.columns.tolist()] + df.values.tolist()
        body = {
            'values': values
        }
        response = sheets.values().update(
            spreadsheetId=spreadsheet_id,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"{response.get('updatedCells')} cells updated.")
        print(f"Data successfully added to spreadsheet")
    except FileNotFoundError:
        print("FileNotFoundError: Service account JSON file not found.")
    except Exception as e:
        print(f"An Error Occured while storing data to google sheets: {e}")

def load_to_postgresql(URL_DB, df):
    """Store data into PostgreSQL database."""
    try:
        engine = create_engine(URL_DB)

        with engine.connect() as conn:
            df.to_sql('products', con=conn, if_exists='append', index=False)
            print("Data successfully added to postgreSQL")
    except ValueError as e:
        print(f"ValueError: DataFrame could not be saved: {e}")
    except Exception as e:
        print(f"An Error Occured while storing data to postgreSQL: {e}")