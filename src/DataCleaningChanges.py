import pandas as pd
import numpy as np

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

# Display the results
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

# Align indices of the original and cleaned DataFrames for comparison
df_original_aligned = df_original.loc[df_cleaned.index]

# Compare columns
diff_a = df_original_aligned['currency'] != df_cleaned['currency']
diff_b = df_original_aligned['currency_symbol'] != df_cleaned['currency_symbol']

# Count the number of differing rows
diff_count_a = diff_a.sum()
diff_count_b = diff_b.sum()

# Display results
print(f"{'Column':<20} | {'Differing Rows':<15}")
print("-" * 35)
print(f"{'currency':<20} | {diff_count_a:<15}")
print(f"{'currency_symbol':<20} | {diff_count_b:<15}")


# Calculate the unique values
unique_occasions = len(df['occasion'].unique())
total_rows = 20

# Display the results in a clean format
print(f"{'Metric':<20} | {'Value':<10}")
print("-" * 35)
print(f"{'Unique Occasions':<20} | {unique_occasions:<10}")
print(f"{'Cleaned Occasions':<20} | {total_rows:<10}")

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
    "price": len(df_original["price"])
}

cleaned_lengths = {
    "price": len(df_cleaned["price"])
}

print(f"{'Column':<10} | {'Original Length':<15} | {'Cleaned Length':<15}")
print("-" * 45)
for column in original_lengths:
    print(f"{column:<10} | {original_lengths[column]:<15} | {cleaned_lengths[column]:<15}")

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

# Align indices of the original and cleaned DataFrames for comparison
df_original_aligned = df_original.loc[df_cleaned.index]

# Compare columns
diff_a = df_original_aligned['dish_id'] != df_cleaned['dish_id']

# Count the number of differing rows
diff_count_a = diff_a.sum()
# Display results
print(f"{'Column':<20} | {'Differing Rows':<15}")
print("-" * 35)
print(f"{'dish_id':<20} | {diff_count_a:<15}")

