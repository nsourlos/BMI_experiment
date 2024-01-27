#Prompt: A folder 'results' has subfolders with files in them. A folder 'details_final' has 2 subfolders 'high' and 'low' 
#with subfolders in them. For each of the subfolders in the 'results' folder, check if the same subfolder name exists within 
#either the 'high' or 'low' folder. If it does, copy the file names within that subfolder inside the same subfolder of the match

import os
import shutil

results_folder = 'C:/Users/soyrl/Desktop/BMI_radiologists_review/results'
details_folder = 'C:/Users/soyrl/Desktop/BMI_radiologists_review/details_final'

# Get a list of subfolders in the 'results' folder
subfolders_results = [folder for folder in os.listdir(results_folder) if os.path.isdir(os.path.join(results_folder, folder))]

# Iterate over each subfolder in 'results'
for subfolder in subfolders_results:
    # Check if the subfolder exists in 'high' or 'low'
    for details_subfolder in ['high', 'low']:
        # Path of the potential matching subfolder
        potential_match = os.path.join(details_folder, details_subfolder, subfolder)
        
        # Check if the potential match exists
        if os.path.exists(potential_match):
            # Get the list of files in the 'results' subfolder
            files_to_copy = os.listdir(os.path.join(results_folder, subfolder))
            
            # Create the destination subfolder if it doesn't exist
            destination_folder = os.path.join(details_folder, details_subfolder, subfolder)
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            
            # Copy each file from 'results' to the matching subfolder
            for file_name in files_to_copy:
                source = os.path.join(results_folder, subfolder, file_name)
                destination = os.path.join(destination_folder, file_name)
                shutil.copy2(source, destination)
            
            # Break out of the loop if a match is found to avoid unnecessary checks
            break
