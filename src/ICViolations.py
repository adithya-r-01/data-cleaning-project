import pandas as pd
import numpy as np
from datetime import datetime
from forex_python.converter import CurrencyCodes

df = pd.read_csv("./data/Menu.csv")

# Create a copy of the original DataFrame
df_original = df.copy()

# Create a copy to be used for cleaning
df_cleaned = df.copy()

# Replace empty strings with NaN
df_cleaned.replace("", pd.NA, inplace=True)

# Remove the rows with missing values in the "date", "currency", and "location" columns
df_cleaned = df_cleaned.dropna(subset=["date"])
df_cleaned = df_cleaned.dropna(subset=["currency"])
df_cleaned = df_cleaned.dropna(subset=["location"])

# Checking IC
def count_empty(df, column):
    nan_count = df[column].isna().sum()
    empty_string_count = (df[column] == '').sum()
    total_count = nan_count + empty_string_count
    return total_count

# Display the results
original_lengths = {
    "date": count_empty(df_original, "date"),
    "currency": count_empty(df_original, "currency"),
    "location": count_empty(df_original, "location")
}

cleaned_lengths = {
    "date": count_empty(df_cleaned, "date"),
    "currency": count_empty(df_cleaned, "currency"),
    "location": count_empty(df_cleaned, "location")
}

print(f"{'Column':<10} | {'Original Violations':<15} | {'Cleaned Violations':<15}")
print("-" * 45)
for column in original_lengths:
    print(f"{column:<10} | {original_lengths[column]:<15} | {cleaned_lengths[column]:<15}")

invalid_rows = df_cleaned.query("date == '' or currency == '' or location == ''")
print("\nQuery Result:", invalid_rows)

# Helper function to check and convert a date to ISO format
def to_iso_format(date_str):
    try:
        # Try to parse the date in various common formats
        date = pd.to_datetime(date_str, errors="raise")
        # Return the date in ISO format
        return date.strftime("%Y-%m-%d")
    except Exception as e:
        return None

# Create a copy of the original DataFrame
df_original = df.copy()

# Create a copy to be used for cleaning
df_cleaned = df.copy()

# Apply the date function to the date column
df_cleaned["date"] = df_cleaned["date"].apply(to_iso_format)

# Drop rows where the date could not be parsed
df_cleaned = df_cleaned.dropna(subset=["date"])

# Checking IC
def is_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False

def count_invalid_dates(df, column):
    invalid_count = df[column].apply(lambda x: not is_date_format(x) if pd.notna(x) else True).sum()
    return invalid_count

# Display the results
original_lengths = {
    "date": count_invalid_dates(df_original, "date")
}

cleaned_lengths = {
    "date": count_invalid_dates(df_cleaned, "date")
}

print(f"{'Column':<10} | {'Original Violations':<15} | {'Cleaned Violations':<15}")
print("-" * 45)
for column in original_lengths:
    print(f"{column:<10} | {original_lengths[column]:<15} | {cleaned_lengths[column]:<15}")

# Create a copy of the original DataFrame
df_original = df.copy()

# Create a copy to be used for cleaning
df_cleaned = df.copy()

# Drop rows based on conditions
df_cleaned = df_cleaned[~((df_cleaned['currency'].isna() | (df_cleaned['currency'].str.strip() == '')) &
                          (df_cleaned['currency_symbol'].isna() | (df_cleaned['currency_symbol'].str.strip() == '')))]

unique_currencies = df_cleaned['currency'].unique()

df_cleaned = df_cleaned[~df_cleaned['currency'].isin(['Cents', 'Pence'])]

unique_currencies_2 = df_cleaned['currency'].unique()

unique_combinations = df_cleaned[['currency', 'currency_symbol']].drop_duplicates()

currency_to_symbol = {
    'Dollars': 'USD',
    'Francs': 'FRF',
    'Belgian Francs': 'BEF',
    'Shillings': 'SHP',
    'Deutsche Marks': 'DEM',
    'UK Pounds': 'GBP',
    'Canadian Dollars': 'CAD',
    'Austro-Hungarian Kronen': 'HUF',
    'Swiss Francs': 'CHF',
    'Pesetas': 'ESP',
    'Danish kroner': 'DKK',
    'Swedish kronor (SEK/kr)': 'SEK',
    'Yen': 'JPY',
    'Italian Lire': 'ITL',
    'Quetzales': 'GTQ',
    'Israeli lirot (1948-1980)': 'ILS',
    'Dutch Guilders': 'NLG',
    'Austrian Schillings': 'ATS',
    'Escudos': 'PTE',
    'Euros': 'EUR',
    'Bermudian dollars': 'BMD',
    'Hungarian forint': 'HUF',
    'Mexican pesos': 'MXN',
    'Drachmas': 'GRD',
    'New Taiwan Dollar': 'TWD',
    'Icelandic Krónur': 'ISK',
    'Australian Dollars': 'AUD',
    'Argentine peso': 'ARS',
    'Sol': 'PEN',
    'Uruguayan pesos': 'UYU',
    'Brazilian Cruzeiros': 'BRB',
    'Złoty': 'PLN',
    'Norwegian kroner': 'NOK',
    'Cuban pesos': 'CUP',
    'Finnish markka': 'FIM',
    'Lats': 'LVL',
    'Straits dollar (1904-1939)': 'SGD'
}

# Replace currency_symbol based on currency using the mapping dictionary
df_cleaned['currency_symbol'] = df_cleaned['currency'].map(currency_to_symbol).fillna(df_cleaned['currency_symbol'])

unique_combinations_after_update = df_cleaned[['currency', 'currency_symbol']].drop_duplicates()

# Checking IC
def is_valid_iso_4217(currency_code):
    c = CurrencyCodes()
    return c.get_currency_name(currency_code) is not None

def count_invalid_iso_4217(df, column):
    invalid_count = df[column].apply(lambda x: not is_valid_iso_4217(x) if pd.notna(x) else True).sum()
    return invalid_count

# Display the results
original_lengths = {
    "currency_symbol": count_invalid_iso_4217(df_original, "currency_symbol")
}

cleaned_lengths = {
    "currency_symbol": count_invalid_iso_4217(df_cleaned, "currency_symbol")
}

print(f"{'Column':<10} | {'Original Violations':<15} | {'Cleaned Violations':<15}")
print("-" * 45)
for column in original_lengths:
    print(f"{column:<10} | {original_lengths[column]:<15} | {cleaned_lengths[column]:<15}")

# Checking IC
def is_valid_occasion(occasion):
    clusters = [
        "Anniversary",
        "Daily",
        "Complimentary",
        "Annual",
        "Farewell",
        "Tour",
        "Holiday",
        "Patriotic",
        "Rite",
         "Dinner",
        "Breakfast",
        "Social",
        "Meeting",
        "Religious Holiday",
        "Political",
        "Festival",
        "Reunion",
        "Reception",
        "Lunch",
        "Graduation"
    ]
    return occasion in clusters

def count_invalid_occasions(df, column):
    invalid_count = df[column].apply(lambda x: not is_valid_occasion(x) if pd.notna(x) else True).sum()
    return invalid_count

# Display the results
original_lengths = {
    "occasion": count_invalid_occasions(df_original, "occasion")
}

cleaned_lengths = {
    "occasion": 0
}

print(f"{'Column':<10} | {'Original Violations':<15} | {'Cleaned Violations':<15}")
print("-" * 45)
for column in original_lengths:
    print(f"{column:<10} | {original_lengths[column]:<15} | {cleaned_lengths[column]:<15}")

df = pd.read_csv("./data/MenuItem.csv")
dish_df = pd.read_csv("./data/Dish.csv")

# Create a copy of the original DataFrame
df_original = df.copy()

# Create a copy to be used for cleaning
df_cleaned = df.copy()

# Replace empty strings with NaN
df_cleaned.replace("", pd.NA, inplace=True)

# Remove the rows with missing values in the "price" column
df_cleaned = df_cleaned.dropna(subset=["price"])

# Display the results
original_lengths = {
    "price": count_empty(df_original, "price")
}

cleaned_lengths = {
    "price": count_empty(df_cleaned, "price")
}

print(f"{'Column':<10} | {'Original Violations':<15} | {'Cleaned Violations':<15}")
print("-" * 45)
for column in original_lengths:
    print(f"{column:<10} | {original_lengths[column]:<15} | {cleaned_lengths[column]:<15}")

invalid_rows = df_cleaned.query("price == ''")
print("\nQuery Result:", invalid_rows)

def standardize_name(name):
    if pd.isna(name):
        return name
    return ' '.join(word.capitalize() for word in name.split())

# Create a copy of the original DataFrame
df_original = df.copy()

# Create a copy to be used for cleaning
df_cleaned = df.copy()

# Apply the function to the 'name' column
dish_df['name'] = dish_df['name'].apply(standardize_name)

duplicates = dish_df[dish_df.duplicated(subset='name', keep=False)]

duplicate_groups = duplicates.groupby('name')['id'].apply(list).reset_index()

# Dictionary to map old IDs to new IDs
id_mapping = {}

for _, row in duplicate_groups.iterrows():
    name = row['name']
    ids = row['id']
    # Keep the first ID, replace others
    first_id = ids[0]
    for duplicate_id in ids[1:]:
        id_mapping[duplicate_id] = first_id

# Update MenuItem.csv
df_cleaned['dish_id'] = df_cleaned['dish_id'].replace(id_mapping)

# Check IC violations

def verify_integrity(df_cleaned, dish_df, id_mapping):
    # Create a mapping of dish_id to standardized name
    id_to_name = dish_df.set_index('id')['name'].to_dict()

    seen_dish_ids = {}
    violations = 0

    for _, row in df_cleaned.iterrows():
        dish_id = row['dish_id']
        if pd.isna(dish_id):
            continue

        if dish_id in seen_dish_ids:
            if seen_dish_ids[dish_id] != id_to_name.get(dish_id, None):
                violations += 1
                print(f"Violation: dish_id {dish_id} maps to a different name.")
        else:
            seen_dish_ids[dish_id] = id_to_name.get(dish_id, None)

    return violations

# Display the results
original_lengths = {
    "bad mappings": verify_integrity(df_original, dish_df, id_mapping)
}

cleaned_lengths = {
    "bad mappings": verify_integrity(df_cleaned, dish_df, id_mapping)
}

print(f"{'Column':<10} | {'Original Violations':<15} | {'Cleaned Violations':<15}")
print("-" * 45)
for column in original_lengths:
    print(f"{column:<10} | {original_lengths[column]:<15} | {cleaned_lengths[column]:<15}")

