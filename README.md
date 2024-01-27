# BMI experiment files

![Alt text](./bmi-experiment.svg)

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![forthebadge](https://forthebadge.com/images/badges/uses-badges.svg)](https://forthebadge.com)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-no-red.svg)](https://github.com/nsourlos/BMI_experiment)


# [Results](./reviewing_info_extract_BMI.ipynb)

> This repo contains the code needed to perform the BMI experiment. 


## Table of Contents
- [General Information](#general-information)
- [Steps](#steps)
- [Patient Selection](#patient-selection)
- [Main Script](#main-script)

## General Information
**For this experiment, the file that needs to be executed is the [reviewing_info_extract_BMI](./reviewing_info_extract_BMI.ipynb)**

This will also execute [patient_selection_BMI_experiment](./patient_selection_BMI_experiment.ipynb). 

The process for this experiment was different from the [emphysema](https://github.com/nsourlos/emphysema_experiment). In the current experiment, we had two radiologists separately and blindly reviewed the findings. 

The following folders are needed before running any files:

- A folder (`BMI_exp_files`) with the Excel files created from the comparison of REDCap and AI output using the [automatic comparison algorithm](https://github.com/nsourlos/Siemens_AIRadCompanion_automatic_comparison). There should be 2 Excel files, one for low and one for high BMI participants.
- A folder (`detailed_final`) containing two subfolders, low and high, each having subfolders with patient IDs and inside them a screenshot of the nodule and a txt file with the results of the radiologist review. 
- A folder (`redcap_levels`) having an Excel file with the REDCap database with all nodules and their characteristics for the participants of our experiment
- Two Excel files with the radiologists' reviews. For step 4 these two files should have the findings in the same order. 
- Another CSV file to obtain demographics from it 

A detailed description of each step can be found below. These should run before the [reviewing_info_extract_BMI](./reviewing_info_extract_BMI.ipynb) file to ensure that the results are correct. Most of the above files are not included in this repository for privacy reasons. 

## Steps

- [Step 0](./0.no_details_to_details.py): Updates an Excel file with detailed information based on the files in a directory.
This script first reads an Excel file containing participant IDs and slice numbers of findings that should be reviewed by radiologists. It then checks if a subfolder with the participant ID exists in a specific directory. If the subfolder exists, it searches for a file whose first 3 letters match the slice number in the Excel. If a matching file is found, it extracts the next 2 letters from the file name and replaces the slice number in the Excel with the previous slice number followed by `_` and the extracted letters.
If only one matching file is found, the function appends `fp` or `fn` to the extracted letters based on their presence in the file name. If multiple matching files are found, the function appends `fp` or `fn` and a number depending on the number of occurrences.
The script at the end removes unnecessary columns from the Excel file and saves the updated file.

- [Step 0a](./0a.review_discrepancies.py): This script reads two Excel files (assuming they are located in a specified directory), and performs the following operations:
1. For each row in the second file, it extracts the values of the columns `participant_id` and the first 3 digits of `slice_number`.
2. It checks if there are any rows in the first file with the same values (only considering the first 3 characters of `slice_number`).
3. If a matching row is found, it replaces the values of all columns (except `participant_id` and `slice_number`) in the first file
with the corresponding values from the second file.
4. If no matching row is found, it keeps track of the unmatched rows and appends the values of the corresponding columns from the second file to the common columns of the first file.
5. It removes columns with `Unnamed` and `previous_review` in the name from the first file.
6. It replaces the last occurrence of the substring `_fp` with `fp` and `_fn` with `fn` in the `slice_number` column of the first file.
7. It saves the updated first file to a new Excel file named `final_BMI_review.xlsx`.

- [Step 1](./1.excel_to_txt.py): Converts an Excel file (created in the previous step) with participant information into text files.
For each participant_id in that file, a subfolder in the `results` folder is created.
Multiple text files per participant are being created depending on the number of slices with findings.
Each text file contains the `type_of_finding`, `details_of_finding`, and confidence for each `slice_number`. That way, it is ensured that we have the same information there as in the emphysema experiment. 


- [Step 2](./2.combine_txt_with_images.py): Copies txt files from subfolders in the `results` folder to the subfolders `low` and `high` in the `details_final` folder. For each of the subfolders in the `results` folder, it checks if the same subfolder name exists within either the `high` or `low` folder. If it does, it copies the files within that subfolder to the same subfolder of the match. By running this step we can have the images of the findings that were reviewed by the radiologists in that same folder too.

- [Step 3](./3.Redcap_to_BMI_levels_folders.py): Split the given dataframe into two new dataframes based on the values in the `participant_id` column.
Each new dataframe will contain only the rows where the `participant_id` value exists in the corresponding folder.

- [Step 4](./4.BMI_excel_comparison.py): Compare two Excel files with the reviews of the two radiologists (assuming they have the same order). The files have a column named `type_of_finding` that takes integer values. This function compares the values of `type_of_finding` in each row and prints the `participant_id` and `slice_number` columns for the rows where these values differ between the two Excel files. It also saves the differences in a new Excel file. These are the findings that have to be reviewed by a third radiologist to establish a ground truth. 



[rename_blind_reading_&_export_to_excel_for_review](./rename_blind_reading_&_export_to_excel_for_review.ipynb): This code renames files in a directory based on certain conditions and exports them to Excel for review. It can be used for performing a blind review (not inform radiologists if the finding was a `fp` or `fn`).

The code iterates through the folders and subfolders in a given path. For each file in the subfolders, 
if the file name contains `fp` or `fn`, it renames the file by appending a number to the original name. 
If the renamed file already exists in the subfolder, it increments the number until a unique name is found.

If the renamed file does not exist in the subfolder, it renames the file by replacing the original name 
with a new name that starts with the first three characters of the original name.

After renaming the files, the code exports them to an Excel file for review.


## [Patient Selection](./patient_selection_BMI_experiment.ipynb)

This code performs data processing and analysis on BMI data obtained from REDCap.
It imports necessary dependencies, reads excel files, combines dataframes, performs data cleaning and manipulation,
and extracts information for further analysis. The code also includes comments explaining the changes made compared to a previous experiment.


### Usage
- This code requires the execution of a previous notebook (`reviewing_info_extract.ipynb`) to load necessary dictionaries that contain information about FN findings.


More specifically:

1. This Python script processes data related to Body Mass Index (BMI) from REDCap files. Among others, it reads and combines data from different BMI degrees, identifies inconsistencies, analyzes BMI severity, and extracts true positive information.
2. It reads Excel files containing data for high and low BMI from specified paths. It appends the data to create a DataFrame named `BMI_data`.
3. It performs various data preprocessing steps, including handling inconsistencies, combining BMI dataframes, and creating severity columns. It also deletes specific nodules based on participant ID.
4. Identifies and handles inconsistencies in the data, such as participants with fewer volumes than nodules found.
5. Analyzes BMI severity by creating a severity column and sorting the data by severity.
6. Extracts true positive information from REDCap data based on manually checked annotations. It initializes dictionaries to store participant IDs and their corresponding true positive nodules.
7. Extracts true positive information for the IDs of TP nodules for each participant. Converts REDCap IDs to numbers from 1-10 that correspond to REDCap attributes.
8. Adds information from REDCap to lists, including calcification, pfn, attachment, and nodule type. The script creates and populates dictionaries with participant IDs, nodule IDs, slices, and volumes.

**Note**: Please replace placeholder values such as `low_pats` and `high_pats` with the actual patient IDs.

The next section is designed to extract and categorize information about true positive (TP) or false negative (FN) nodules from REDCap data. It processes data related to lung nodules, classifying them into different categories based on various attributes.

More specifically:

#### **Function: TP_info_redcap**

This function extracts information about TP or FN nodules from REDCap. It categorizes nodules based on attributes such as calcification, pleural attachment, nodule type, and more. The categorization includes various subgroups like calcified nodules, pleural nodules, ground glass nodules, atypical periphysural fissural nodules, peribronchial lymph nodes, and others.

#### Parameters

- `tp_or_fn` (optional): Specifies whether to extract information for TP (true positive) or FN (false negative) nodules. Default is 'tp'.

#### Output

The function updates global variables for different nodule categories, storing information about each nodule's participant ID, nodule number, slices, and volumes.

#### **Function: errors_check**

This function checks for errors in REDCap data entry. It ensures that all nodules are correctly categorized and that there are no missing or duplicate entries.

#### Parameters

- `tp_or_fn` (optional): Specifies whether to check errors for TP (true positive) or FN (false negative) nodules. Default is 'tp'.

#### Output

The function performs error checks and prints information about missing or incorrectly categorized nodules. It also corrects certain errors, deleting entries from one category and adding them to another.

After the above, the code uses global variables to store categorized nodules, making them accessible outside the functions.
The script includes detailed error checking and correction for data entry issues.

More specifically, the next part of the code processes data related to the detection of nodules and lymph nodes in medical imaging. It focuses on categorizing true positive (TP) and false negative (FN) findings based on certain criteria and performs various analyses on these findings.

#### Atypical Lymph Nodes and Nodule Groups
- Atypical lymph nodes are considered as nodules.
- Nodule group names are defined as follows:
  - `nod_groups_only`: ['sub_ground', 'pleural', 'calcified', 'other_all', 'atypical_triangular']
  - `lymph_groups`: ['per_fisu', 'peri_bronch']

#### TP Analysis for Nodules and Lymph Nodes
The code iterates over low and high BMI levels to analyze TP findings for nodules and lymph nodes. It calculates the total number of findings, volumes, and categorizes them based on volume ranges.

#### Nodule Groups Analysis
- Iterates over `nod_groups_only`.
- Calculates the total number of findings, volumes in the ranges 30-100, 100-300, and 300+ mm³.
- Saves the results to pickle files for further use.

#### Lymph Node Analysis
- Iterates over `lymph_groups`.
- Calculates the total number of findings, volumes in the ranges 30-100, 100-300, and 300+ mm³.
- Saves the results to pickle files for further use.

#### Total TP Findings and Participants
- Prints the total number of TP findings and the number of participants for low and high BMI levels.

#### False Negative (FN) Analysis
Identifies participants with at least one FN based on certain volume subgroups. Extracts relevant information for further analysis.

#### Slice Matching and Consensus Review
Compares initial readings with consensus reviews for FN findings. It identifies discrepancies and prints details for manual checking.

#### Additional Functionality
- Extracts and matches slices with participant IDs for FN findings.
- Handles dictionaries of FN findings, separating correct and incorrect entries.
- Detects and handles errors related to duplicate slices.



## [Main Script](./reviewing_info_extract_BMI.ipynb)

This script analyzes the results of a nodule review conducted by radiologists. It processes the text files containing review details and categorizes findings into nodule and non-nodule categories. The analysis includes false positives (FP), false negatives (FN), and true positives (TP) for various nodule types and non-nodule findings. Additionally, confidence scores and participant-specific information are collected.

#### File Paths
- `path_high`: Path to the folder containing subfolders with individuals of high BMI.
- `path_low`: Path to the folder containing subfolders with individuals of low BMI.

#### Data Reading
The script reads data from two Excel files (`high_scans.xlsx` and `low_scans.xlsx`) located in the `BMI_exp_files` directory. These files contain relevant information for the analysis.

#### Function: `show_information_of_review(path)`
This function processes the nodule review information in the specified path. It prints participant IDs, file details (slice number and if it is a FP or FN), confidence scores, and findings descriptions. The function categorizes findings into different nodule and non-nodule types and tracks FP, FN, and TP counts.

### Categories Analyzed
#### Nodule Categories
1. Calcified Nodules
2. Pleural Nodules
3. Other Nodules
4. Subsolid/Ground Glass Nodules
5. Cancer Cases
6. Atypical PFN and/or Triangular Lymph Nodes
7. Perifissural/Fissural/PFN
8. Bronchiovascular Lymph Nodes

#### Non-Nodule Categories
1. Fibrosis/Scar/Pleural Thickening
2. Other Findings (Bone, Tissue, Mucus, Arthrosis, Vessel, Consolidation, Infection, Fat, Atelectasis, etc.)

#### Result Summary
- Counts of FPs, FNs, and TPs for each category.
- Total number of analyzed files.
- Mean and median confidence scores.

#### Important Notes
- The function excludes files with low confidence (<=3).
- Some categories have subcategories, and the function distinguishes between correct and wrong classifications for detailed analysis.

#### Documentation of next steps
The next part of the code includes steps for data preprocessing and replacement of specific values to ensure accurate calculations. It involves replacing certain markers (`!!!` and `xxx`) and handling volumes of AI nodules based on defined criteria.

The code then converts slices to IDs, addresses issues with the automated algorithm output, and handles cases with errors - replaces zero volumes with NaN values.

The next step is to perform participant-level analysis for FPs, focusing on different volume subgroups. It initializes empty dictionaries and populates them with corresponding FP information.

The code includes a section for manual checks, identifying participants with nodules not reviewed by radiologists. It lists participants that require manual inspection to ensure accurate mapping of slices to IDs.


Then there is a correction of errors and manual addition of participants for whom a unique mapping wasn't possible.
Atypical lymph nodes are considered as nodules in the main experiment.
Special consideration is given to atypical PFNs being treated as lymph nodes in the subanalysis.

The code then checks for consistency in False Positives (FP) between different dictionaries containing participant IDs. The focus is on participants with low and high BMI.

For each BMI degree, the script manually corrects errors in the dict_FP_wrong and dict_FP_correct dictionaries by replacing values with '-'.
Participants with only '-' values in these dictionaries are deleted.
Similar operations are performed for dictionaries related to lymph nodes (`lymph_FP_wrong`) and nodules (`nod_FP_wrong`) for each BMI degree.
Specific errors might be checked and deleted from the nodule list for particular cases (`dict_FP_correct_high['686142']`).
Then, it counts non-nodules, lymph nodes, and nodules for both low and high BMI cases and prints the total number of False Positives (FP) and True Positives (TP) for low and high BMI. The same checks are repeated for participants with both low and high BMI, with an additional check for consistency between lymph nodes and nodules.

The results are further organized based on different volume subgroups (30-100 mm³, 100-300 mm³, 300+ mm³) for both FP and FN cases. Additionally, the code performs statistical tests, such as Mann-Whitney U tests, to compare the performance of the AI system and the human reader in different BMI groups and volume subgroups.

#### Final Steps and Table Creation

1. **Loading Data:**
   - The code loads participant IDs, volumes, and other attributes related to false negatives from pickle files.
   - Separate data loading is performed for different categories, including false negatives with correct and wrong findings, for both low and high BMI groups.

2. **Initializing Counters and Lists:**
   - Counters and lists are initialized to keep track of occurrences of non-nodules, nodules, and lymph nodes in various BMI and volume subgroups.
   - Lists are created to store volumes associated with each category and subgroup for statistical analysis.

3. **Processing False Negatives:**
   - The code iterates through loaded data to categorize and count false negatives based on BMI, volume, and finding type.
   - Volumes are categorized into subgroups based on predefined criteria (e.g., volume between 30-100, 100-300, >300 mm^3).
   - Counts and volumes are aggregated for different BMI and volume subgroups.

4. **Generating Detailed Comparison Tables:**
   - Detailed comparison tables are created for false positives and false negatives, specifically for low and high BMI groups.
   - Different categories of findings (e.g., fibrosis/scar, other non-nodules) are presented, with total counts and percentages.

5. **Exporting Results to Excel:**
   - The code exports the detailed comparison tables to Excel files for further analysis and visualization.

The final sections focus on creating the tables used in the manuscript, performing statistical comparisons and an analysis on a volume basis and on a type-of-finding basis. For the statistical analysis and confidence interval calculations some functions are defined based on information found in literature. In total the same tables/results are reported twice, once with and once without inclusion of benign lymph nodes (PFNs).


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

 
## License
[MIT License](LICENSE)
