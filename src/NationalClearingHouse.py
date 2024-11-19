import pandas as pd
import numpy as np

NCH_file_path = r"C:\Users\ge144\Desktop\Projects\NationalClearingHouse\data\Clearninghouse_Raw Data.xlsx"
RU_file_path = r"C:\Users\ge144\Desktop\Projects\NationalClearingHouse\data\RU Class of 2024 Grad Terms.xlsx"


try:
    # Read the "NCH_file_path" sheet
    nch_df = pd.read_excel(NCH_file_path, sheet_name='in', engine='openpyxl')

    # Read the "RU_file_path" sheet
    ru_df = pd.read_excel(RU_file_path, sheet_name='RU Grad Term Lookup', engine='openpyxl')
    
except Exception as e:
    print(f"Error reading the Excel file: {e}")
    df_raw, df_skeleton = None, None

try:
    # Convert 'Enrollment Begin' and 'Enrollment End' in nch_df
    nch_df['Enrollment Begin'] = pd.to_datetime(nch_df['Enrollment Begin'], format='%Y%m%d')
    nch_df['Enrollment End'] = pd.to_datetime(nch_df['Enrollment End'], format='%Y%m%d')
    nch_df['Graduation Date'] = pd.to_datetime(nch_df['Graduation Date'], format='%Y%m%d', errors='coerce')


    # Convert 'Class of 2024 Grad Term' in ru_df (make sure to use the correct column name)
    ru_df['Class of 2024 Grad Term'] = pd.to_datetime(ru_df['Class of 2024 Grad Term'], format='%b %y')


    # Sort nch_df by 'First Name', then 'Enrollment Begin', and then 'Graduation Date' when 'Enrollment Begin' and 'Enrollment End' are empty
    nch_sorted_df = nch_df.sort_values(
        by=['First Name', 'Enrollment Begin', 'Enrollment End', 'Graduation Date'],
        key=lambda col: col.isnull().astype(int) if col.name in ['Enrollment Begin', 'Enrollment End'] else col
    )

    
    # Perform a merge with suffixes to handle overlapping columns
    joined_df = pd.merge(
        nch_df,
        ru_df,
        left_on='Requester Return Field',
        right_on='ClearingHouse Unique ID',
        how='left',
        suffixes=('_nch', '_ru')  # Adding suffixes to differentiate overlapping columns
    )

    # Filter rows where 'Enrollment Begin' is greater than 'Class of 2024 Grad Term'
    filtered_df = joined_df[joined_df['Enrollment Begin'] > joined_df['Class of 2024 Grad Term']]

    print(joined_df[['First Name_nch', 'Enrollment Begin', 'Enrollment End', 'Graduation Date','Class of 2024 Grad Term']])
    print(filtered_df[['First Name_nch','Last Name_nch', 'Enrollment Begin', 'Enrollment End', 'Graduation Date','Class of 2024 Grad Term']])

except Exception as e:
    print(f"Error: {e}")

