import pandas as pd

def transform_and_clean_data(data):
    """Convert data into dataframe and transform data"""
    try:
        df = pd.DataFrame(data)

        # Delete all duplicates and null/NaN/None
        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)
        
        # Delete Product Title == "Unknown Product"
        df = df.drop(df[df["Title"] == "Unknown Product"].index)

        # Transform Product Price
        try:
            df = df.drop(df[df["Price"] == "Price Unavailable"].index)
            df["Price"] = df["Price"].str.replace("$", "", regex=False).astype(float)
            df["Price"] = (df["Price"] * 16000).astype(float)
        except (AttributeError, ValueError, KeyError) as e:
            print(f"Error while transforming Price: {e}")

        # Transform Product Rating
        try:
            df = df[~df["Rating"].str.contains("Invalid|Not Rated", na=False)]
            df["Rating"] = df["Rating"].str.extract(r'(\d+(?:\.\d+)?)').astype(float)
        except (AttributeError, ValueError, KeyError) as e:
            print(f"Error while transforming Rating: {e}")

        # Transform colors
        try:
            df["Colors"] = df["Colors"].str.extract(r'(\d+)').astype(int)
        except (AttributeError, ValueError, KeyError) as e:
            print(f"Error transforming Colors: {e}")

        # Transform Size
        df["Size"] = df["Size"].str.replace("Size: ", "")

        # Transform Gender
        df["Gender"] =df["Gender"].str.replace("Gender: ", "")
    except Exception as e:
        print(f"General error in transform_and_clean_data: {e}")

    return df