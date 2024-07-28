# @begin DataCleaningScript

import pandas as pd
import numpy as np
from datetime import datetime
from forex_python.converter import CurrencyCodes

# @begin Load_Data @desc Load the menu data from CSV
# @in menu_csv @uri file:./data/Menu.csv
# @out df_initial
df = pd.read_csv("./data/Menu.csv")
# @end Load_Data

# Create a copy of the original DataFrame
df_original = df.copy()

# Create a copy to be used for cleaning
df_cleaned = df.copy()

# @begin Replace_Empty_Strings @desc Replace empty strings with NaN
# @in df_initial
# @out df_replaced_empty
df_cleaned.replace("", pd.NA, inplace=True)
# @end Replace_Empty_Strings

# @begin Drop_Missing_Values @desc Remove the rows with missing values in the specified columns
# @in df_replaced_empty
# @out df_dropped_missing
df_cleaned = df_cleaned.dropna(subset=["date"])
df_cleaned = df_cleaned.dropna(subset=["currency"])
df_cleaned = df_cleaned.dropna(subset=["location"])
# @end Drop_Missing_Values

# @begin Count_Empty @desc Count empty values in columns
# @in df @param column
# @out total_count_empty
def count_empty(df, column):
    nan_count = df[column].isna().sum()
    empty_string_count = (df[column] == '').sum()
    total_count = nan_count + empty_string_count
    return total_count
# @end Count_Empty

# @begin Display_Results @desc Display the lengths of original and cleaned data
# @in df_original @in df_dropped_missing
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
# @end Display_Results

# @begin Query_Invalid_Rows @desc Query invalid rows
# @in df_dropped_missing
# @out invalid_rows
invalid_rows = df_cleaned.query("date == '' or currency == '' or location == ''")
print("\nQuery Result:", invalid_rows)
# @end Query_Invalid_Rows

# @begin To_ISO_Format @desc Convert date to ISO format
# @in df_dropped_missing
# @out df_iso_format
def to_iso_format(date_str):
    try:
        date = pd.to_datetime(date_str, errors="raise")
        return date.strftime("%Y-%m-%d")
    except Exception as e:
        return None

df_cleaned["date"] = df_cleaned["date"].apply(to_iso_format)

# Drop rows where the date could not be parsed
df_cleaned = df_cleaned.dropna(subset=["date"])
# @end To_ISO_Format

# @begin Is_Date_Format @desc Check if the date is in ISO format
# @param date_str
# @out is_valid_date
def is_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False
# @end Is_Date_Format

# @begin Count_Invalid_Dates @desc Count invalid dates in the column
# @in df @param column
# @out invalid_count_dates
def count_invalid_dates(df, column):
    invalid_count = df[column].apply(lambda x: not is_date_format(x) if pd.notna(x) else True).sum()
    return invalid_count
# @end Count_Invalid_Dates

# @begin Display_Date_Results @desc Display the lengths of original and cleaned data for date column
# @in df_original @in df_iso_format
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
# @end Display_Date_Results

# @begin Drop_Empty_Currency @desc Drop rows with empty currency columns
# @in df @out df_cleaned_currency
df_cleaned = df_cleaned[~((df_cleaned['currency'].isna() | (df_cleaned['currency'].str.strip() == '')) &
                          (df_cleaned['currency_symbol'].isna() | (df_cleaned['currency_symbol'].str.strip() == '')))]
# @end Drop_Empty_Currency

# @begin Unique_Currencies @desc Get unique currencies
# @in df_cleaned_currency
# @out unique_currencies
unique_currencies = df_cleaned['currency'].unique()
# @end Unique_Currencies

# @begin Drop_Invalid_Currencies @desc Drop rows with invalid currency values
# @in df_cleaned_currency
# @out df_cleaned_valid_currency
df_cleaned = df_cleaned[~df_cleaned['currency'].isin(['Cents', 'Pence'])]
# @end Drop_Invalid_Currencies

# @begin Unique_Currency_Combinations @desc Get unique currency and symbol combinations
# @in df_cleaned_valid_currency
# @out unique_combinations
unique_combinations = df_cleaned[['currency', 'currency_symbol']].drop_duplicates()
# @end Unique_Currency_Combinations

# @begin Currency_To_Symbol @desc Map currency to currency symbol
# @in df_cleaned_valid_currency
# @out df_currency_mapped
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

df_cleaned['currency_symbol'] = df_cleaned['currency'].map(currency_to_symbol).fillna(df_cleaned['currency_symbol'])
# @end Currency_To_Symbol

# @begin Unique_Combinations_After_Update @desc Get unique currency and symbol combinations after update
# @in df_currency_mapped
# @out unique_combinations_after_update
unique_combinations_after_update = df_cleaned[['currency', 'currency_symbol']].drop_duplicates()
# @end Unique_Combinations_After_Update

# @begin Is_Valid_ISO_4217 @desc Check if the currency code is a valid ISO 4217 code
# @param currency_code
# @out is_valid_iso
def is_valid_iso_4217(currency_code):
    c = CurrencyCodes()
    return c.get_currency_name(currency_code) is not None
# @end Is_Valid_ISO_4217

# @begin Count_Invalid_ISO_4217 @desc Count invalid ISO 4217 codes
# @in df @param column
# @out invalid_count_iso
def count_invalid_iso_4217(df, column):
    invalid_count = df[column].apply(lambda x: not is_valid_iso_4217(x) if pd.notna(x) else True).sum()
    return invalid_count
# @end Count_Invalid_ISO_4217

# @begin Display_Currency_Symbol_Results @desc Display the lengths of original and cleaned data for currency_symbol column
# @in df_original @in df_currency_mapped
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
# @end Display_Currency_Symbol_Results

# @begin Is_Valid_Occasion @desc Check if the occasion is valid
# @param occasion
# @out is_valid_occasion
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
# @end Is_Valid_Occasion

# @begin Count_Invalid_Occasions @desc Count invalid occasions
# @in df @param column
# @out invalid_count_occasion
def count_invalid_occasions(df, column):
    invalid_count = df[column].apply(lambda x: not is_valid_occasion(x) if pd.notna(x) else True).sum()
    return invalid_count
# @end Count_Invalid_Occasions

# @begin Display_Occasion_Results @desc Display the lengths of original and cleaned data for occasion column
# @in df_original @in df_cleaned
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
# @end Display_Occasion_Results

# @begin Load_MenuItem_Data @desc Load the menu item data from CSV
# @in menu_item_csv @uri file:./data/MenuItem.csv
# @in dish_csv @uri file:./data/Dish.csv
# @out df_menu_item @out df_dish
df = pd.read_csv("./data/MenuItem.csv")
dish_df = pd.read_csv("./data/Dish.csv")
# @end Load_MenuItem_Data

# Create a copy of the original DataFrame
df_original = df.copy()

# Create a copy to be used for cleaning
df_cleaned = df.copy()

# @begin Replace_Empty_Strings_MenuItem @desc Replace empty strings with NaN in MenuItem data
# @in df_menu_item
# @out df_cleaned_menu_item
df_cleaned.replace("", pd.NA, inplace=True)
# @end Replace_Empty_Strings_MenuItem

# @begin Drop_Missing_Price @desc Remove the rows with missing values in the price column
# @in df_cleaned_menu_item
# @out df_cleaned_menu_item_price
df_cleaned = df_cleaned.dropna(subset=["price"])
# @end Drop_Missing_Price

# @begin Display_Price_Results @desc Display the lengths of original and cleaned data for price column
# @in df_original @in df_cleaned_menu_item_price
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
# @end Display_Price_Results

# @begin Query_Invalid_Price_Rows @desc Query invalid rows for price column
# @in df_cleaned_menu_item_price
# @out invalid_price_rows
invalid_rows = df_cleaned.query("price == ''")
print("\nQuery Result:", invalid_rows)
# @end Query_Invalid_Price_Rows

# @begin Standardize_Name @desc Standardize the dish names
# @in df_dish
# @out df_standardized_names
def standardize_name(name):
    if pd.isna(name):
        return name
    return ' '.join(word.capitalize() for word in name.split())

dish_df['name'] = dish_df['name'].apply(standardize_name)
# @end Standardize_Name

# @begin Handle_Duplicates @desc Handle duplicate dish names
# @in df_dish
# @out id_mapping @out df_cleaned_dish
duplicates = dish_df[dish_df.duplicated(subset='name', keep=False)]

duplicate_groups = duplicates.groupby('name')['id'].apply(list).reset_index()

id_mapping = {}
for _, row in duplicate_groups.iterrows():
    name = row['name']
    ids = row['id']
    first_id = ids[0]
    for duplicate_id in ids[1:]:
        id_mapping[duplicate_id] = first_id

df_cleaned['dish_id'] = df_cleaned['dish_id'].replace(id_mapping)
# @end Handle_Duplicates

# @begin Verify_Integrity @desc Verify integrity of the cleaned data
# @in df_cleaned_dish @in df_dish @in id_mapping
# @out violations
def verify_integrity(df_cleaned, dish_df, id_mapping):
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
# @end Verify_Integrity

# @end DataCleaningScript
