#Prompt:given an excel file, take its first column ('participant_id') and its second ('slice_number'). For each participant id check in 
# a folder if there is a subfolder with that id as its name. If exists, check inside it if there is a file, the first 3 letters of which 
# are the slice_number of the same row of the excel. If found, get the next 2 letters of that file and replace slice number in the excel 
# with the previous slice number and then '_' and the next 2 letters

#Got relatively good results but had to make changes. On top of the above I also modified it with the following: 

#Count how many such files exist. If one found, get the next 3 letters of that file and replace slice number in the excel with the 
# previous slice number and then '_' and then 'fp' or 'fn' depending on which one of those exist in the letters. If more than one found, 
# replace slice number in the excel with the previous slice number and then '_' and then 'check'

import os
import pandas as pd

# Read the excel file
df = pd.read_excel('C:/Users/soyrl/Desktop/BMI_radiologists_review/BMI_to_review_original_with_changes_GdJ.xlsx')

files_checked=[] #Keep track of files with more than one match

# Iterate over each row
for index, row in df.iterrows():
    participant_id = str(row['participant_id'])
    slice_number = str(row['slice_number']) #Due to manual changes this might be int

    # Check if the directory exists
    dir_path = f'C:/Users/soyrl/Desktop/BMI_radiologists_review/detailed/{participant_id}'
    if os.path.isdir(dir_path):
        # Search for a file with the given prefix
        files = os.listdir(dir_path)
        matching_files = [f for f in files if f.startswith(slice_number)]
        
        #Check if files have less than 3 digits - Add 0 in front since there will be slices <100
        for ind,file in enumerate(matching_files):
            if file[:3].isnumeric():
                pass
            else:
                print(matching_files[ind])
                matching_files[ind]='0'+matching_files[ind][:2]+matching_files[ind][2:]

        if len(matching_files) == 1: #if only one file
            matching_file = matching_files[0]
            
            suffix = matching_file[3:5] if matching_file[3:5] in ['fp', 'fn'] else ''

            # Extract the slice number and update it with 'fp' or 'fn' 
            new_slice_number = f"{slice_number}_{suffix}"
            df.at[index, 'slice_number'] = new_slice_number
            
        else: #if more than one file
            for ind2,file_match in enumerate(matching_files): #loop over them

                print("many matches",file_match,'is',file_match[3:5])

                if ind2+index in files_checked: #if already checked, skip
                    pass
                else:
                    if ind2==0: #if zero index, not include it in the name
                        new_slice_number = f"{slice_number[:3]}_{file_match[3:5]}"
                    else: #if any other value include it in the name
                        if len(file_match)==9: #For cases with just slice number and 'fp' or 'fn' like '216fp.png'
                            new_slice_number = f"{slice_number[:3]}_{file_match[3:5]}"
                        else: #For all other cases in which we might have eg. '216_1fp'
                            new_slice_number = f"{slice_number[:3]}_{str(ind2)}{file_match[3:5]}"
                    
                    df.at[index+ind2, 'slice_number'] = new_slice_number
                    files_checked.append(ind2+index) #add to list of checked files


#Columns to remove
rem_cols=[col for col in df.columns if col.startswith('Unnamed')]

#Remove columns
df.drop(columns=rem_cols, inplace=True)

# Save the updated excel file
df.to_excel('C:/Users/soyrl/Desktop/BMI_radiologists_review/BMI_differences_reviewed_modified_with_details_all.xlsx', index=False)