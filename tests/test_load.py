import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql

@pytest.fixture
def test_df():
    return pd.DataFrame({
        'Title': ['T-shirt 2', 'Crewneck 7'], 
        'Price': [1634400.0, 6892000.0], 
        'Rating': [3.9, 4.3], 
        'Colors': [3, 3], 
        'Size': ['M', 'M'], 
        'Gender': ['Women', 'Men'], 
        'Timestamp': ['2025-04-27T18:42:22.587022', '2025-04-27T19:37:50.109322'] 
    })

def load_to_csv_success(test_df, tmp_path):
    """Test storing the dataframe to CSV without error"""
    file_path = tmp_path / "output.csv"
    load_to_csv(str(file_path), test_df)

    assert file_path.exists()

    df_loaded = pd.read_csv(file_path)
    assert not df_loaded.empty
    assert list(df_loaded.columns) == list(test_df.columns)

@patch("utils.load.Credentials.from_service_account_file")
@patch("utils.load.build")
def test_load_to_google_sheets_success(mock_build, mock_credentials, test_df):
    """Test storing dataframe to google sheets successfully"""
    mock_service = MagicMock()
    mock_sheets = mock_service.spreadsheets.return_value
    mock_values = mock_sheets.values.return_value
    mock_values.update.return_value.execute.return_value = {'updatedCells': 10}

    mock_build.return_value = mock_service
    mock_credentials.return_value = MagicMock()

    load_to_google_sheets('fake_spreadsheet_id', test_df)

    mock_build.assert_called_once()
    mock_sheets.values.assert_called_once()
    mock_values.update.assert_called_once()

@patch("utils.load.create_engine")
@patch("pandas.DataFrame.to_sql")
def test_load_to_postgresql_success(mock_to_sql, mock_create_engine, test_df):
    """Test load_to_postgresql stores data correctly using SQLAlchemy"""
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_create_engine.return_value = mock_engine

    load_to_postgresql('postgresql://testuser:password@localhost/productsdb', test_df)

    mock_create_engine.assert_called_once()
    mock_engine.connect.assert_called_once()
    mock_to_sql.assert_called_once_with(
        'products', con=mock_conn, if_exists='append', index=False
    )