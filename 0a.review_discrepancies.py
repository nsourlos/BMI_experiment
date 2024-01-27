#Given two Excel files 'BMI_to_review_GdJ_final_vols_checked_and_removed' and 'BMI_differences_reviewed', 
# for each row in the second file get the values of the columns 'participant_id' and of the first 3 digits of 'slice_number'. 
# Try to find if there are any rows in the other df with the same values (only check the first 3 characters of 'slice_number' in it). 
#  If there is a row with the same values, replace the values of all columns other than 'participant_id and 'slice_number' in that row
#  of the 'BMI_to_review_GdJ_final_vols_checked_and_removed' with those of the 'BMI_differences_reviewed' of the matched row. 
# If there are none, keep track of them and at the end append the values of the corresponding columns of 'BMI_differences_reviewed' 
# of that row in the common columns of 'BMI_to_review_GdJ_final_vols_checked_and_removed' 

import pandas as pd
import os

# Read the two Excel files into dataframes
df1 = pd.read_excel(os.getcwd()+'/Desktop/BMI_radiologists_review/'+'BMI_to_review_GdJ_final_vols_checked_and_removed.xlsx')
df2 = pd.read_excel(os.getcwd()+'/Desktop/BMI_radiologists_review/'+'BMI_differences_reviewed_modified_with_details_all.xlsx')

# Create a list to store the rows from df2 that have no match in df1
unmatched_rows = []

# Iterate through each row in df2
for index, row in df2.iterrows():
    # Extract 'participant_id' and first 3 characters of 'slice_number' from df2
    participant_id = row['participant_id']

    slice_number_prefix = str(row['slice_number'])

    # Check if there are rows in df1 with the same values
    matching_rows = df1[(df1['participant_id'] == participant_id) & (df1['slice_number'].astype(str) == slice_number_prefix)] 

    if len(matching_rows) == 0:
        # If no matching rows found, add the row from df2 to the unmatched_rows list
        unmatched_rows.append(row)

    else:
        # If matching rows found, update the values in df1 with the values from df2
        for col in df1.columns:
            if col not in ['participant_id', 'slice_number'] and 'Unnamed' not in col and 'previous_review' not in col:
                df1.loc[matching_rows.index, col] = row[col]

# Append the values from unmatched_rows to df1
if len(unmatched_rows) > 0:
    df1 = df1.append(unmatched_rows, ignore_index=True)

#Remove columns with 'Unnamed' and 'previous_review' in the name
filtered_columns = [col for col in df1.columns if 'Unnamed' not in col and 'previous_review' not in col] 
df_filtered = df1[filtered_columns]

# Remove the last occurrence of the substring in each row
df_filtered['slice_number'] = df_filtered['slice_number'].str.replace('_fp', 'fp')
df_filtered['slice_number'] = df_filtered['slice_number'].str.replace('_fn', 'fn')

# Save the updated df1 back to an Excel file if needed
df_filtered.to_excel(os.getcwd()+'/Desktop/BMI_radiologists_review/'+'final_BMI_review.xlsx', index=False)