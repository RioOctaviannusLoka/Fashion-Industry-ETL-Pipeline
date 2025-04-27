from utils.extract import scrape_products
from utils.transform import transform_and_clean_data
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql

URL = 'https://fashion-studio.dicoding.dev'
filename = "products.csv"
spreadsheet_id = "1dLOqZyBfcn_p2yVBI8KC3pFlDkF7FMOuTyXWZbFBRVs"

username = "developer"
password = "supersecretpassword"
host = "localhost"
port = "5432"
db_name = "productsdb"
URL_DB = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}'

all_products = scrape_products(URL)

if all_products:
    df = transform_and_clean_data(all_products)
    
    load_to_csv(filename, df)
    load_to_google_sheets(spreadsheet_id, df)
    load_to_postgresql(URL_DB, df)