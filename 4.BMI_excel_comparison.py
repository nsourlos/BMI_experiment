#Prompt: Two excel files named 'BMI_to_review_GdJ' and 'BMI_to_review_original_schalekamp' can be found in Desktop. 
# Both have a column named 'type_of_finding' that takes integer values. Compare one by one these values and print 
# the value of the 'participant_id' and 'slice_number' columns for the rows in which these values differ

import pandas as pd
import os

# Load the Excel files into pandas DataFrames -'BMI_to_review_original_GdJ.xlsx' to create file to be reviewed by a 3rd radiologist
file1_path = os.getcwd()+'/Desktop/BMI_radiologists_review/BMI_to_review_GdJ_final_vols_checked_and_removed.xlsx' 
file2_path = os.getcwd()+'/Desktop/BMI_radiologists_review/BMI_to_review_schalekamp_final_vols_checked_and_removed.xlsx'
df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)

# Filter rows where 'type_of_finding' values differ
differing_rows = df1[(df1['type_of_finding'] != df2['type_of_finding'])]# & ((df1['type_of_finding'] == 3) 
#  & (df2['type_of_finding'] == 1))] #& added to find non-nodule rows by one of the radiologists

differing_rows_steven=df2[(df1['type_of_finding'] != df2['type_of_finding'])]

num_of_diffs = 0

df_dif_review=pd.DataFrame(columns=['participant_id','slice_number','previous_review','type_of_finding','details_of_finding','confidence'])

# Print the values of 'participant_id' and 'slice_number' for differing rows
ind=0 #index for Gonda's dataframe
for _, row in differing_rows.iterrows():
    num_of_diffs += 1
    participant_id = row['participant_id']
    slice_number = row['slice_number']
    confidence_gonda = row['confidence']
    confidence_steven = differing_rows_steven.iloc[ind]['confidence']
    review_gonda=row['type_of_finding']
    review_steven=differing_rows_steven.iloc[ind]['type_of_finding']
    ind+=1

    if review_gonda==1:
        review_gonda='nodule'
    elif review_gonda==2:
        review_gonda='non-nodule'
    elif review_gonda==3:
        review_gonda='lymph node'

    if review_steven==1:
        review_steven='nodule'
    elif review_steven==2:
        review_steven='non-nodule'
    elif review_steven==3:
        review_steven='lymph node'
    
    # print(f"Participant ID: {participant_id}, Slice Number: {slice_number}, Confidence Gonda {confidence_gonda}, Confidence Steven {confidence_steven}")
    df_dif_review=df_dif_review.append({'participant_id':participant_id,'slice_number':slice_number,
                                        'previous_review':str(review_gonda)+'/'+str(review_steven),
                                        'type_of_finding':'','details_of_finding':'','confidence':''},ignore_index=True)

print("Total number of differences: ", num_of_diffs)
#There are 50 non-nodules/lymph nodes, 40 nodules/lymph nodes, 19 non-nodules/nodules, 1 missing value

#Save the new review file
df_dif_review.to_excel(os.getcwd()+'/Desktop/BMI_radiologists_review/BMI_to_review_differences_with_info.xlsx',index=False) 


#Repeat above analysis to find common rows
common_rows = df1[(df1['type_of_finding'] == df2['type_of_finding'])]
common_rows_steven=df2[(df1['type_of_finding'] == df2['type_of_finding'])]

num_of_common = 0

df_common_review=pd.DataFrame(columns=['participant_id','slice_number','previous_review','type_of_finding'])#,'details_of_finding','confidence'])

ind=0 #index for common dataframe
for _, row in common_rows.iterrows():
    num_of_common += 1
    participant_id = row['participant_id']
    slice_number = row['slice_number']
    # confidence_gonda = row['confidence']
    # confidence_steven = common_rows_steven.iloc[ind]['confidence']
    review_gonda=row['type_of_finding']
    # review_steven=common_rows_steven.iloc[ind]['type_of_finding']
    gonda_details=row['details_of_finding']
    steven_details=common_rows_steven.iloc[ind]['details_of_finding']

    ind+=1

    if review_gonda==1:
        review_gonda='nodule'
    elif review_gonda==2:
        review_gonda='non-nodule'
    elif review_gonda==3:
        review_gonda='lymph node'

    # if review_steven==1:
    #     review_steven='nodule'
    # elif review_steven==2:
    #     review_steven='non-nodule'
    # elif review_steven==3:
    #     review_steven='lymph node'
    
    # print(f"Participant ID: {participant_id}, Slice Number: {slice_number}")#, Confidence Gonda {confidence_gonda}, Confidence Steven {confidence_steven}")
    df_common_review=df_common_review.append({'participant_id':participant_id,'slice_number':slice_number,
                                        'previous_review':str(review_gonda),#+'/'+str(review_steven),
                                        'type_of_finding':''},ignore_index=True) #,'details_of_finding':'','confidence':''}
    

    print(f"Participant ID: {participant_id}, Slice Number: {slice_number}, Confidence Gonda {confidence_gonda}, Confidence Steven {confidence_steven}, \
          Gonda details {gonda_details}, Steven details {steven_details}")

print("Total number of common findings: ", num_of_common)

#Save the new review file
df_common_review.to_excel(os.getcwd()+'/Desktop/BMI_radiologists_review/BMI_to_review_common_with_info.xlsx',index=False)

#Save both the above files to one excel file
combined_df = pd.concat([df_common_review, df_dif_review], ignore_index=True)
combined_df.to_excel(os.getcwd()+'/Desktop/BMI_radiologists_review/BMI_reviewed_all_final.xlsx',index=False)
#242 common findings, 96 differences