import pandas as pd

country_dict_path = "/home/acct/schaf/team/yiyid/projects/data_vit/Infiles/country_dictionary_clean_2505.csv"
p27_data_path = "/home/acct/schaf/team/yiyid/projects/data_vit/Infiles/20240411 P27 yearly.dta"
output_path = "/home/acct/schaf/team/yiyid/projects/data_vit/Infiles/20240411_P27_with_region.csv"

country_df = pd.read_csv(country_dict_path)
p27_df = pd.read_stata(p27_data_path)

original_rows, original_cols = p27_df.shape
print(f"Original P27 file: {original_rows} rows, {original_cols} columns")

# Drop duplicates and rows with missing ISIN
p27_df = p27_df.drop_duplicates()
print(f"After deduplication: {len(p27_df)} rows")

p27_df = p27_df[pd.notna(p27_df['isin'])]
print(f"After dropping rows with missing ISIN: {len(p27_df)} rows")

# Check uniqueness of key fields
key_cols = ['isin', 'ccode', 'fips', 'iso2c', 'year', 'panel_id']
duplicates_p27 = p27_df.duplicated(subset=key_cols, keep=False)
n_duplicates_p27 = duplicates_p27.sum()

if n_duplicates_p27 == 0:
    print("Key combinations are unique in the original file.")
else:
    print(f"{n_duplicates_p27} rows have duplicate key combinations in the original file.")

# Prepare for merge
country_df['country_lower'] = country_df['country'].str.lower()
p27_df['country_name_text_lower'] = p27_df['country_name_text'].str.lower()

region_info = country_df[['country_lower', 'region', 'country_clean']]
merged_df = p27_df.merge(
    region_info,
    left_on='country_name_text_lower',
    right_on='country_lower',
    how='left'
)

# Clean up
merged_df.drop(columns=['country_lower', 'country_name_text_lower'], inplace=True)

# Drop duplicates after merge
before_dedup = len(merged_df)
merged_df = merged_df.drop_duplicates()
after_dedup = len(merged_df)
print(f"After merge deduplication: {before_dedup} → {after_dedup} rows")

duplicates_merged = merged_df.duplicated(subset=key_cols, keep=False)
n_duplicates_merged = duplicates_merged.sum()

if n_duplicates_merged == 0:
    print("Key combinations are unique after merge.")
else:
    print(f"{n_duplicates_merged} rows have duplicate key combinations after merge.")

missing_region = merged_df['region'].isna().sum()
final_rows, final_cols = merged_df.shape

print(f"Final file saved to: {output_path}")
print(f"Final shape: {final_rows} rows, {final_cols} columns")
print(f"Rows with missing region: {missing_region}")

merged_df.to_csv(output_path, index=False)

