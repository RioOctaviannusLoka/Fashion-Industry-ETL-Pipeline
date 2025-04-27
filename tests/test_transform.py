import pytest
import pandas as pd
from utils.transform import transform_and_clean_data

@pytest.fixture
def test_data():
    return [
        {
            'Title': 'Unknown Product', 
            'Price': '$100.00', 
            'Rating': 'Rating: ⭐ Invalid Rating / 5', 
            'Colors': '5 Colors', 
            'Size': 'Size: M', 
            'Gender': 'Gender: Men', 
            'Timestamp': '2025-04-27T18:42:22.587022'
        }, 
        {
            'Title': 'T-shirt 2', 
            'Price': '$102.15', 
            'Rating': 'Rating: ⭐ 3.9 / 5', 
            'Colors': '3 Colors', 
            'Size': 'Size: M', 
            'Gender': 'Gender: Women', 
            'Timestamp': '2025-04-27T18:42:22.587022'}, 
        {
            'Title': 'Pants 16', 
            'Price': 'Price Unavailable', 
            'Rating': 'Rating: Not Rated', 
            'Colors': '8 Colors', 
            'Size': 'Size: S', 
            'Gender': 'Gender: Men', 
            'Timestamp': '2025-04-27T18:42:22.602623'
        },
        {
            'Title': 'Pants 4', 
            'Price': '$467.31', 
            'Rating': 'Rating: ⭐ Invalid Rating / 5', 
            'Colors': '3 Colors', 
            'Size': 'Size: XL', 
            'Gender': 'Gender: Men', 
            'Timestamp': '2025-04-27T18:42:22.587022'
        }, 
        {
            'Title': 'Outerwear 5', 
            'Price': '$321.59', 
            'Rating': 'Rating: ⭐ 3.5 / 5', 
            'Colors': None, 
            'Size': None, 
            'Gender': None, 
            'Timestamp': '2025-04-27T18:42:22.587022'
        }
    ]

def test_transform_data_success(test_data):
    df_result = transform_and_clean_data(test_data)

    assert not df_result.empty
    expected_columns = ["Title", "Price", "Rating", "Colors", "Size", "Gender", "Timestamp"]
    assert all(col in df_result.columns for col in expected_columns)
    
    assert not (df_result["Title"] == "Unknown Product").any()
    assert pd.api.types.is_object_dtype(df_result["Title"])

    assert not (df_result["Price"] == "Price Unavailable").any()
    assert pd.api.types.is_float_dtype(df_result["Price"])

    assert not (df_result["Rating"] == "Rating: ⭐ Invalid Rating / 5").any()
    assert not (df_result["Rating"] == "Rating: Not Rated").any()
    assert pd.api.types.is_float_dtype(df_result["Rating"])
    
    assert pd.api.types.is_integer_dtype(df_result["Colors"])

    assert not df_result["Size"].str.contains("Size: ").any()
    assert pd.api.types.is_object_dtype(df_result["Size"])

    assert not df_result["Gender"].str.contains("Gender: ").any()
    assert pd.api.types.is_object_dtype(df_result["Gender"])

    assert pd.api.types.is_object_dtype(df_result["Timestamp"])