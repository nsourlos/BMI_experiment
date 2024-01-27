#Prompt: An excel file with the following columns is given as input: 'participant_id','slice_number','type_of_finding',
# 'details_of_finding','confidence'. Create a folder named 'results', having subfolders with each participant id in it. 
# Inside each of those subfolders create txt files, one for each slice_number of that participant. In each txt file, write the following
#  information: type_of_finding, details_of_finding,confidence

import os
import pandas as pd

# Read the input Excel file
df = pd.read_excel('C:/Users/soyrl/Desktop/BMI_radiologists_review/final_BMI_review.xlsx') 

# Create the results folder if it doesn't exist
if not os.path.exists('C:/Users/soyrl/Desktop/BMI_radiologists_review/results'):
    os.mkdir('C:/Users/soyrl/Desktop/BMI_radiologists_review/results')

# Loop through each participant id
for participant_id in df['participant_id'].unique():

    # Create a subfolder for the participant if it doesn't exist
    participant_folder = os.path.join('C:/Users/soyrl/Desktop/BMI_radiologists_review/results', str(participant_id))
    if not os.path.exists(participant_folder):
        os.mkdir(participant_folder)

    # Loop through each slice_number for the participant
    for slice_number in df.loc[df['participant_id'] == participant_id, 'slice_number'].unique():

        # Get the relevant rows for this slice_number and participant_id
        slice_df = df.loc[(df['participant_id'] == participant_id) & (df['slice_number'] == slice_number)]

        # Create a txt file for this slice_number
        filename = os.path.join(participant_folder, f'{slice_number}.txt')

        # Write the type_of_finding, details_of_finding, and confidence to the txt file
        with open(filename, 'w') as f:
            for _, row in slice_df.iterrows():

                try: #In case not integer as type of finding we will get an error
                    
                    #Replace integer value with the actual type of finding
                    if int(row['type_of_finding'])==1:
                        f.write(f"{'nodule'} ")
                    elif int(row['type_of_finding'])==2:
                        f.write(f"{'no nodule'} ")
                    elif int(row['type_of_finding'])==3:
                        f.write(f"{'no nodule lymph node'} ")
                    else: #In case a different integer
                        print("Wrong type of finding for participant", participant_id, "type of finding value is",row['type_of_finding'])
                
                except: #In case error print participant and value of that field
                    print("Some error in participant", participant_id, "type of finding is",row['type_of_finding'])

                f.write(f"{row['details_of_finding']} {(row['confidence'])}\n") #Add the rest to the txt file