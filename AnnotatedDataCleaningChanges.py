# @begin DataCleaningChangesScript

import pandas as pd
import numpy as np

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

# @begin Drop_Missing_Values @desc Remove rows with missing values in the specified columns
# @in df_replaced_empty
# @out df_dropped_missing
df_cleaned = df_cleaned.dropna(subset=["date"])
df_cleaned = df_cleaned.dropna(subset=["currency"])
df_cleaned = df_cleaned.dropna(subset=["location"])
# @end Drop_Missing_Values

# @begin Display_Results @desc Display the lengths of original and cleaned data
# @in df_original @in df_dropped_missing
original_lengths = {
    "date": len(df_original["date"]),
    "currency": len(df_original["currency"]),
    "location": len(df_original["location"])
}
cleaned_lengths = {
    "date": len(df_cleaned["date"]),
    "currency": len(df_cleaned["currency"]),
    "location": len(df_cleaned["location"])
}
print(f"{'Column':<10} | {'Original Length':<15} | {'Cleaned Length':<15}")
print("-" * 45)
for column in original_lengths:
    print(f"{column:<10} | {original_lengths[column]:<15} | {cleaned_lengths[column]:<15}")
# @end Display_Results

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

# Display the results
original_lengths = {
    "date": len(df_original["date"])
}
cleaned_lengths = {
    "date": len(df_cleaned["date"])
}
print(f"{'Column':<10} | {'Original Length':<15} | {'Cleaned Length':<15}")
print("-" * 45)
for column in original_lengths:
    print(f"{column:<10} | {original_lengths[column]:<15} | {cleaned_lengths[column]:<15}")
# @end To_ISO_Format

# @begin Clean_Currency_Columns @desc Clean and map currency columns
# @in df_iso_format
# @out df_cleaned_currency
df_cleaned = df_cleaned[~((df_cleaned['currency'].isna() | (df_cleaned['currency'].str.strip() == '')) &
                          (df_cleaned['currency_symbol'].isna() | (df_cleaned['currency_symbol'].str.strip() == '')))]

df_cleaned = df_cleaned[~df_cleaned['currency'].isin(['Cents', 'Pence'])]

currency_to_symbol = {
    'Dollars': 'USD',
    'Francs': 'FRF',
    'Belgian_Francs': 'BEF',
    'Shillings': 'SHP',
    'Deutsche_Marks': 'DEM',
    'UK_Pounds': 'GBP',
    'Canadian_Dollars': 'CAD',
    'Austro_Hungarian_Kronen': 'HUF',
    'Swiss_Francs': 'CHF',
    'Pesetas': 'ESP',
    'Danish_kroner': 'DKK',
    'Swedish_kronor_SEK_kr': 'SEK',
    'Yen': 'JPY',
    'Italian_Lire': 'ITL',
    'Quetzales': 'GTQ',
    'Israeli_lirot_1948_1980': 'ILS',
    'Dutch_Guilders': 'NLG',
    'Austrian_Schillings': 'ATS',
    'Escudos': 'PTE',
    'Euros': 'EUR',
    'Bermudian_dollars': 'BMD',
    'Hungarian_forint': 'HUF',
    'Mexican_pesos': 'MXN',
    'Drachmas': 'GRD',
    'New_Taiwan_Dollar': 'TWD',
    'Icelandic_Kronur': 'ISK',
    'Australian_Dollars': 'AUD',
    'Argentine_peso': 'ARS',
    'Sol': 'PEN',
    'Uruguayan_pesos': 'UYU',
    'Brazilian_Cruzeiros': 'BRB',
    'Zloty': 'PLN',
    'Norwegian_kroner': 'NOK',
    'Cuban_pesos': 'CUP',
    'Finnish_markka': 'FIM',
    'Lats': 'LVL',
    'Straits_dollar_1904_1939': 'SGD'
}

df_cleaned['currency_symbol'] = df_cleaned['currency'].map(currency_to_symbol).fillna(df_cleaned['currency_symbol'])
# @end Clean_Currency_Columns

# @begin Compare_Columns @desc Compare columns between original and cleaned DataFrames
# @in df_original @in df_cleaned_currency
# @out diff_count_a @out diff_count_b
df_original_aligned = df_original.loc[df_cleaned.index]
diff_a = df_original_aligned['currency'] != df_cleaned['currency']
diff_b = df_original_aligned['currency_symbol'] != df_cleaned['currency_symbol']
diff_count_a = diff_a.sum()
diff_count_b = diff_b.sum()
print(f"{'Column':<20} | {'Differing Rows':<15}")
print("-" * 35)
print(f"{'currency':<20} | {diff_count_a:<15}")
print(f"{'currency_symbol':<20} | {diff_count_b:<15}")
# @end Compare_Columns

# @begin Calculate_Unique_Occasions @desc Calculate unique occasions
# @in df
# @out unique_occasions
unique_occasions = len(df['occasion'].unique())
total_rows = 20
print(f"{'Metric':<20} | {'Value':<10}")
print("-" * 35)
print(f"{'Unique Occasions':<20} | {unique_occasions:<10}")
print(f"{'Cleaned Occasions':<20} | {total_rows:<10}")
# @end Calculate_Unique_Occasions

# @begin Load_MenuItem_Data @desc Load the menu item data from CSV
# @in menu_item_csv @uri file:./data/MenuItem.csv
# @in dish_csv @uri file:./data/Dish.csv
# @out df_menu_item @out df_dish
df = pd.read_csv("./data/MenuItem.csv")
dish_df = pd.read_csv("./data/Dish.csv")
# @end Load_MenuItem_Data

# @begin Replace_Empty_Strings_MenuItem @desc Replace empty strings with NaN in MenuItem data
# @in df_menu_item
# @out df_cleaned_menu_item
df_cleaned.replace("", pd.NA, inplace=True)
# @end Replace_Empty_Strings_MenuItem

# @begin Drop_Missing_Price @desc Remove rows with missing values in the price column
# @in df_cleaned_menu_item
# @out df_cleaned_menu_item_price
df_cleaned = df_cleaned.dropna(subset=["price"])
original_lengths = {"price": len(df_original["price"])}
cleaned_lengths = {"price": len(df_cleaned["price"])}
print(f"{'Column':<10} | {'Original Length':<15} | {'Cleaned Length':<15}")
print("-" * 45)
for column in original_lengths:
    print(f"{column:<10} | {original_lengths[column]:<15} | {cleaned_lengths[column]:<15}")
# @end Drop_Missing_Price

# @begin Standardize_Name @desc Standardize the dish names
# @in name
# @out standardized_name
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

# @begin Compare_Columns_DishID @desc Compare columns between original and cleaned DataFrames for dish_id
# @in df_menu_item @in df_cleaned_dish
# @out diff_count_dish_id
df_original_aligned = df_original.loc[df_cleaned.index]
diff_a = df_original_aligned['dish_id'] != df_cleaned['dish_id']
diff_count_a = diff_a.sum()
print(f"{'Column':<20} | {'Differing Rows':<15}")
print("-" * 35)
print(f"{'dish_id':<20} | {diff_count_a:<15}")
# @end Compare_Columns_DishID

# @end DataCleaningChangesScript
