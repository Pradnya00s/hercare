import pandas as pd
import os

# Load Excel file
file_path = "pcos_screener/data/PCOS_data_without_infertility.xlsx"
xls = pd.ExcelFile(file_path)

# Load the actual data sheet
df = pd.read_excel(xls, sheet_name="Full_new")

# Drop unnecessary columns (example: unnamed columns, instruction notes, etc.)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Handle missing values (basic example: drop rows with NaN)
df = df.dropna()

# Create new file name with versioning
base_path = "pcos_screener/data/"
version = 1
new_file = f"pcos_clean_v{version}.csv"

# Keep incrementing version if file already exists
while os.path.exists(os.path.join(base_path, new_file)):
    version += 1
    new_file = f"pcos_clean_v{version}.csv"

# Save cleaned dataset
output_path = os.path.join(base_path, new_file)
df.to_csv(output_path, index=False)

print(f"Cleaned dataset saved as {output_path}")
