#prompt: given a dataframe and two folders, split the dataframe to two new ones, each one containing only the rows of the 
# column 'participant_id' where the value of that column exists in each of the folders as subfolder. 

#The below implementations was later modified to take participants from lists since some were missing in those folders

import os
import pandas as pd
import csv
from IPython.display import display
pd.set_option('display.max_rows', None)

#Patient IDs of individuals with low and high BMI
low_pats=[....]

high_pats=[....]

def split_dataframe_by_folders(df, low_pats, high_pats, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get a list of subfolders in folder1
    folder1_subfolders = [str(name) for name in high_pats]
    # Get a list of subfolders in folder2
    folder2_subfolders = [str(name) for name in low_pats]

    df['participant_id_only'] = [str(participant)[:6] for participant in df['participant_id'].values] #New column with IDs only

    # Filter dataframe rows based on subfolder existence
    df_folder1 = df[df['participant_id_only'].isin(folder1_subfolders)]
    df_folder2 = df[df['participant_id_only'].isin(folder2_subfolders)]

    # Save the filtered dataframes as CSV files
    df_folder1.to_csv(os.path.join(output_folder, 'high_redcap.csv'), index=False ,quoting=csv.QUOTE_ALL) #Avoid issues with commas between quotes
    df_folder2.to_csv(os.path.join(output_folder, 'low_redcap.csv'), index=False ,quoting=csv.QUOTE_ALL)

    return


data=[] #Empty list to save the csv file

with open('C:/Users/soyrl/Desktop/BMI_radiologists_review/redcap_levels/BMI_6-6-2023.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

df = pd.DataFrame(data[1:],columns=data[0])

#Rename first column to 'participant_id'
current_column_names = df.columns.tolist()
current_column_names[0] = 'participant_id'
df.columns = current_column_names

output_folder = 'C:/Users/soyrl/Desktop/BMI_radiologists_review/redcap_levels/redcap_output/'  # output folder path
split_dataframe_by_folders(df, low_pats, high_pats, output_folder)