<h1 align="center">Fashion Industry ETL Pipeline</h1>

---

# Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Data Source](#data-source)
- [Tech Stack](#tech-stack)
- [ETL Pipeline Components](#etl-pipeline-components)
- [How to Use](#how-to-use)

# Project Overview

This project implements simple ETL (Extract, Transform, Load) pipeline for scraping data from fashion retail website and transform it into desired format, then load it into CSV flat file, google sheets, and postgresql database. The overall pipeline is designed with a modular architecture, allowing each component or stage of the process to operate independently. This structure not only promotes code reusability and maintainability but also ensures that the workflow can be easily adapted or extended in the future to accommodate additional data sources and analytical tasks.

# Project Structure
```
├── tests/                      # Unit tests directory for the ETL pipeline
│   ├── test_extract.py         # Tests for extraction functionality
│   ├── test_transform.py       # Tests for transformation functionality
│   └── test_load.py            # Tests for loading functionality
├── utils/                      # Core ETL functionality modules
│   ├── extract.py              # Data extraction module (web scraping)
│   ├── transform.py            # Data transformation and cleaning
│   └── load.py                 # Data loading to various destinations
├── .env/                       # Virtual environment (not tracked in git)
├── main.py                     # Main ETL pipeline controller
├── products.csv                # Raw scraped data
├── requirements.txt            # Project dependencies
├── google-sheets-api.json      # Google Sheets API credentials (not tracked in git)
└── README.md                   # Project documentation
```

# Data Source

The data used in this project is scraped from [Fashion Studio Website](https://fashion-studio.dicoding.dev/)

# Tech Stack

<a href="https://www.python.org/"><img src="https://techstack-generator.vercel.app/python-icon.svg" alt="Python Icon" title="Python" width="65" height="65" /></a>
<a href="https://pandas.pydata.org/"><img src="https://go-skill-icons.vercel.app/api/icons?i=pandas" alt="Pandas Icon" title="Pandas" width="65" height="65" /></a>
<a href="https://www.sqlalchemy.org/"><img src="https://go-skill-icons.vercel.app/api/icons?i=sqlalchemy" alt="SQL Alchemy" title="SQL Alchemy" width="65" height="65" /></a>
<a href="https://docs.pytest.org/en/stable/"><img src="https://go-skill-icons.vercel.app/api/icons?i=pytest" alt="Pytest Icon" title="Pytest" width="65" height="65" /></a>
<a href="https://code.visualstudio.com/"><img src="https://go-skill-icons.vercel.app/api/icons?i=vscode" alt="Visual Studio Code" title="Visual Studio Code" width="65" height="65"/></a>

# ETL Pipeline Components

### 1. Extract (`utils/extract.py`)
The extraction module is responsible for scraping product data from [Fashion Studio website](https://fashion-studio.dicoding.dev/). Key functionalities include:
- `fetching_url_content()`: Retrieves raw HTML content from a given URL using the requests library, with custom headers to simulate a browser. Includes error handling for Timeout, RequestException, and HTTP 404 status codes.
- `scrape_products()`: Orchestrates the scraping process across multiple paginated product listing pages. It dynamically handles page navigation and collects product details from each product card into a list.
- `parse_product_details()`: Extracts detailed product information from individual HTML elements, including title, price, rating, number of colors, size, gender, and appends a timestamp to track when the product was scraped.

### 2. Transform (`utils/transform.py`)
The transformation module converts raw scraped data into a structured format and applies necessary data cleaning and transformation steps. Key functionality:
- `transform_and_clean_data()`: Converts the raw data list into a pandas DataFrame and applies the following transformations:
  - Removes duplicates and invalid/missing values.
  - Filters out records with "Unknown Product" titles or "Price Unavailable" prices.
  - Cleans and standardizes the `Price` field:
    - Removes the dollar symbol ($) and converts values to float.
    - Converts the price to local currency (Indonesian Rupiah) using a static exchange rate of 16,000.
  - Extracts numeric values from the `Rating` field using regular expressions.
  - Extracts the number of color options from the `Colors` field (e.g., "5 Colors" → 5).
  - Removes prefixes from the `Size` and `Gender` fields (e.g., "Size: M" becomes "M").



### 3. Load (`utils/load.py`)
The loading module saves the processed data to various destinations:
- `load_to_csv()`: Saves the cleaned data into a local CSV file. Includes exception handling for file path issues or permission errors.
- `load_to_google_sheets()`: Uploads the dataset to a specified Google Sheet using the Google Sheets API and service account credentials. The DataFrame is written starting from cell A1.
- `load_to_postgresql()`: Inserts the final dataset into a PostgreSQL database table named products, using SQLAlchemy for database interaction. If the table exists, new data will be appended.

# How to Use

### Installation

1. Clone this repository

   ```bash
   git clone https://github.com/RioOctaviannusLoka/Fashion-Industry-ETL-Pipeline.git
   ```

2. Install Python Virtual Environment Library

   ```bash
   pip install virtualenv
   ```

3. Create Python Virtual Environment

   Linux / Mac:

   ```bash
   python3 -m virtualenv venv
   ```

   Windows:

   ```bash
   python -m virtualenv venv
   ```

4. Activate the Virtual Environment

   Linux / Mac:

   ```bash
   source venv\bin\activate
   ```

   Windows:

   ```bash
   venv\Scripts\activate
   ```

5. Install all the requirements

   ```bash
   pip install -r requirements.txt
   ```

### Configuration
1. Set up a PostgreSQL database
2. Generate Google Sheets API credentials and save as `google-sheets-api.json`
3. Update database connection parameters and spreadsheet ID in `main.py` if needed

### Run the Pipeline
1. Execute main script to run the ETL pipeline

   Linux / Mac:

   ```bash
   python3 main.py
   ```

    Windows:

    ```bash
    python main.py
    ```

### Unit Testing

1. Run the unit test folder

   Linux / Mac:

   ```bash
   python3 -m pytest tests
   ```

    Windows:

    ```bash
    python -m pytest tests
    ```

2. Run the test coverage report

   ```
   coverage run -m pytest tests
   ```

3. See coverage Report

    ```
    coverage report -m
    ```

### Exit the Virtual Environment

   ```bash
   deactivate
   ```

---

Copyright &copy; 2025 - Rio Octaviannus Loka