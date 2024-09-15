# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
 Quality check for contributions to the Motor Learning Dataset

 Automatically detects files in a given folder: data files (with 'data' in their name), 
 readme files (with 'readme' in their name), and the spreadsheet (.xlsx).

 Instructions:
    - Place this file and all files you're sending in a new folder.
    - When running the file, provide the folder path.
    - The script will automatically find and check the files.
    - Upload your data and results along with the "

--------------------------------------------------------------------------
"""

# directory: /Users/sritejpadmanabhan/Downloads/Research/Motor Learning Project/OpenMotor

import glob
import os
import pandas as pd

# Ask user to input the folder path where all files are located
folder_path = input("Please enter the path to the folder containing your files: ")

# Ensure the path ends with a slash
if not folder_path.endswith('/'):
    folder_path += '/'

''' Get all data files from the folder '''
data_files = sorted(glob.glob(folder_path + '*data*.csv'))
readme_files = sorted(glob.glob(folder_path + '*readme*.txt'))
spreadsheet_files = sorted(glob.glob(folder_path + '*.xlsx'))

# Check if required files were found
if len(spreadsheet_files) == 0:
    raise ValueError('No spreadsheet (.xlsx) file found in the folder.')
if len(data_files) == 0:
    raise ValueError('No data files found in the folder (looking for files with "data" in the name).')
if len(readme_files) == 0:
    raise ValueError('No readme files found in the folder (looking for files with "readme" in the name).')

# Load the first spreadsheet found (assuming only one is required)
T = pd.read_excel(spreadsheet_files[0])
n_datasets = len(T)
names_in_spreadsheet = sorted(list(T.Name_in_database))

''' Determine if equal number of files are present in the spreadsheet, data, and readme '''
num_names = len(names_in_spreadsheet)
num_data = len(data_files)
num_readme = len(readme_files)
numList = [num_names, num_data, num_readme]

print(f'# entries in spreadsheet: {num_names}')
print(f'# data files: {num_data}')
print(f'# readme files: {num_readme}')

if not all([n == numList[0] for n in numList]):
    raise ValueError('ERROR. Number of files doesn\'t match!\n')
else:
    print('OK: Number of files matches.\n')


''' Determine if all names match '''
for dataset_num, data_file in enumerate(data_files):
    spreadsheetname = names_in_spreadsheet[dataset_num]
    datafilename = os.path.basename(data_file).split('.')[0][5:]  # Remove path and extract name
    readmename = os.path.basename(readme_files[dataset_num]).split('.')[0][7:]  # Same for readme

    match_spreadsheet_datafile = spreadsheetname == datafilename
    match_spreadsheet_readme = spreadsheetname == readmename

    if not(match_spreadsheet_datafile) or not(match_spreadsheet_readme):
        print(f'Name in spreadsheet: {spreadsheetname}')
        print(f'Name in data files: {datafilename}')
        print(f'Name in readme files: {readmename}')
        raise ValueError('ERROR. Name doesn\'t match!\n')

print('OK: Names are consistent between the files and the spreadsheet.\n')


''' Determine if data are loading well and if fields are named correctly '''
print('\n-----Checking if the data are loading well and if data columns have correct names.------')

pd.set_option('display.max_columns', 500)  # Force pandas to show 500 columns

for dataset_num, datafile in enumerate(data_files):
    # Load the dataset
    dataframe = pd.read_csv(datafile)

    # Display how the data is being read in
    print(f'\nDataset name: {names_in_spreadsheet[dataset_num]}')
    print('This is how the data from this dataset are being read in:')
    print(dataframe.head(8))  # Show first 8 rows
    print('Please check that columns that should be numeric are indeed numeric.')
    print('If not, this most likely indicates a problem with the formatting of the data.')

    # List of all expected columns
    required_columns = [
        'Subj_idx', 'trial_number', 'target_angle', 'feedback_type', 'rotation_angle',
        'hand_angle', 'reaction_time', 'movement_time', 'search_time', 'screen_height',
        'screen_width', 'repeat_number', 'researcher_id', 'condition', 'block_number',
        'research_setting', 'input_device', 'subject_age', 'subject_sex', 'subject_race',
        'neuro_condition', 'neuro_description', 'years_of_education', 'subject_vision',
        'dominant_hand', 'device_type', 'mouse_type', 'feedback_time', 'initial_x', 
        'initial_y', 'number_of_targets', 'target_type', 'target_height', 'target_width', 
        'target_x', 'target_y', 'clamp_size', 'rotation_direction', 'hand_flip', 
        'hand_base', 'hand_max_velocity', 'cognitive_assessment', 'cognitive_assessment_score'
    ]

    # Check if all required fields are present and give warnings if not
    for column in required_columns:
        if column not in dataframe.keys():
            raise ValueError(f'ERROR. No field "{column}" exists. A field "{column}" MUST be present in the dataset.')

print('')

''' Determine if number of subjects are reported correctly in spreadsheet '''
print('\n-----Checking if reported number of subjects is correct.------')
for dataset_num, datafile in enumerate(data_files):
    # Load the dataset
    dataframe = pd.read_csv(datafile)

    # Get number of subjects from different sources
    numsubj_spreadsheet = T.Num_subjects[dataset_num]
    numsubj_datafile = len(set(dataframe.Subj_idx))

    # Display basic info
    print(f'Dataset name: {names_in_spreadsheet[dataset_num]}')
    print(f'Number of subjects reported in spreadsheet: {numsubj_spreadsheet}')
    print(f'Number of actual subjects in data: {numsubj_datafile}\n')

    # Check for inconsistency in number of subjects
    if numsubj_spreadsheet != numsubj_datafile:
        raise ValueError('ERROR. Number of subjects doesn\'t match between spreadsheet and actual data.')


''' Determine if number of trials per subject are reported correctly in spreadsheet '''
print('\n-----Checking if reported number of trials per subject is correct.------')
for dataset_num, datafile in enumerate(data_files):
    # Load the dataset
    dataframe = pd.read_csv(datafile)

    # Determine the number of trials per subject
    subject_names = sorted(list(set(dataframe.Subj_idx)))
    trials_per_subj = [
            len(dataframe.trial_number[dataframe.Subj_idx == subjname]) for subjname in subject_names]

    # Display basic info
    print(f'Dataset name: {names_in_spreadsheet[dataset_num]}')
    print(f'Min total trials per subject reported in spreadsheet: {T.Min_trials_per_subject[dataset_num]}')
    print(f'Min total trials per subject in the actual data: {min(trials_per_subj)}\n')
    print(f'Max total trials per subject reported in spreadsheet: {T.Max_trials_per_subject[dataset_num]}')
    print(f'Max total trials per subject in the actual data: {max(trials_per_subj)}\n')

    # Check for inconsistency in number of trials per subject
    if T.Min_trials_per_subject[dataset_num] != min(trials_per_subj):
        raise ValueError('ERROR. The min total trials per subject doesn\'t match between spreadsheet and actual data.')
    if T.Max_trials_per_subject[dataset_num] != max(trials_per_subj):
        raise ValueError('ERROR. The max total trials per subject doesn\'t match between spreadsheet and actual data.')
    

def write_confirmation_file(message, output_file):
    """ Write the confirmation or error message to a text file """
    with open(output_file, 'w') as file:
        file.write(message)
    print(f"File '{output_file}' has been created. You can download it from your folder.")

def create_error_message(error_info):
    """ Create the content for the error message """
    message = f"ERROR encountered during quality check: {error_info}\n"
    message += "Please review the following guidelines to fix the issue:\n"
    message += "1. Ensure the data, readme, and spreadsheet files match in number and names.\n"
    message += "2. Check that all required fields are present in the dataset.\n"
    message += "3. Make sure the number of subjects and trials per subject match the spreadsheet report.\n"
    return message
    

def create_success_message(num_datasets, num_subjects, dataset_names):
    """ Create a success message with detailed information """
    message = "Congratulations! Your data passed the quality check.\n"
    message += "Please attach this confirmation message to your submission.\n"
    message += "\nBelow is a summary of your submission:\n"
    message += f"- Number of datasets: {num_datasets}\n"
    message += f"- Total number of subjects: {num_subjects}\n"
    message += f"- Dataset names: {', '.join(dataset_names)}\n"
    message += "\nPlease confirm that the information above is correct. If anything seems wrong, please make corrections before submitting.\n"
    return message


def write_confirmation_file(message, output_file):
    """ Write the confirmation or error message to a text file """
    with open(output_file, 'w') as file:
        file.write(message)
    print(f"File '{output_file}' has been created. You can download it from your folder.")

def create_error_message(error_info):
    """ Create the content for the error message """
    message = f"ERROR encountered during quality check: {error_info}\n"
    message += "Please review the following guidelines to fix the issue:\n"
    message += "1. Ensure the data, readme, and spreadsheet files match in number and names.\n"
    message += "2. Check that all required fields are present in the dataset.\n"
    message += "3. Make sure the number of subjects and trials per subject match the spreadsheet report.\n"
    return message

def create_success_message(num_datasets, num_subjects, dataset_names):
    """ Create a success message with detailed information """
    message = "Congratulations! Your data passed the quality check.\n"
    message += "Please attach this confirmation message to your submission.\n"
    message += "\nBelow is a summary of your submission:\n"
    message += f"- Number of datasets: {num_datasets}\n"
    message += f"- Total number of subjects: {num_subjects}\n"
    message += f"- Dataset names: {', '.join(dataset_names)}\n"
    message += "\nPlease confirm that the information above is correct. If anything seems wrong, please make corrections before submitting.\n"
    return message

# Get all data files from the folder
data_files = sorted(glob.glob(folder_path + '*data*.csv'))
readme_files = sorted(glob.glob(folder_path + '*readme*.txt'))
spreadsheet_files = sorted(glob.glob(folder_path + '*.xlsx'))

# Check if required files were found
if len(spreadsheet_files) == 0:
    error_message = 'No spreadsheet (.xlsx) file found in the folder.'
    write_confirmation_file(create_error_message(error_message), folder_path + "Error_Message.txt")
    raise ValueError(error_message)

if len(data_files) == 0:
    error_message = 'No data files found in the folder (looking for files with "data" in the name).'
    write_confirmation_file(create_error_message(error_message), folder_path + "Error_Message.txt")
    raise ValueError(error_message)

if len(readme_files) == 0:
    error_message = 'No readme files found in the folder (looking for files with "readme" in the name).'
    write_confirmation_file(create_error_message(error_message), folder_path + "Error_Message.txt")
    raise ValueError(error_message)

# Load the first spreadsheet found (assuming only one is required)
T = pd.read_excel(spreadsheet_files[0])
n_datasets = len(T)
names_in_spreadsheet = sorted(list(T.Name_in_database))

# Check if the number of datasets, data files, and readme files match
num_names = len(names_in_spreadsheet)
num_data = len(data_files)
num_readme = len(readme_files)

if not all([n == num_names for n in [num_data, num_readme]]):
    raise ValueError('ERROR. Number of files doesn\'t match!\n')

# Check if names match between the spreadsheet, data files, and readme files
for dataset_num, data_file in enumerate(data_files):
    spreadsheetname = names_in_spreadsheet[dataset_num]
    datafilename = os.path.basename(data_file).split('.')[0][5:]  # Remove path and extract name
    readmename = os.path.basename(readme_files[dataset_num]).split('.')[0][7:]  # Same for readme

    if not(spreadsheetname == datafilename and spreadsheetname == readmename):
        raise ValueError(f'ERROR. Name doesn\'t match for dataset {spreadsheetname}!\n')

# Gather detailed information for the confirmation message
num_datasets = len(data_files)
num_subjects = sum([len(set(pd.read_csv(datafile).Subj_idx)) for datafile in data_files])
dataset_names = names_in_spreadsheet
# Gather detailed information for the confirmation message
num_datasets = len(data_files)
num_subjects = sum([len(set(pd.read_csv(datafile).Subj_idx)) for datafile in data_files])
dataset_names = names_in_spreadsheet
num_readme_files = len(readme_files)
num_spreadsheet_files = len(spreadsheet_files)

# Create the success confirmation message including all relevant details
success_message = "Congratulations! Your data passed the quality check.\n"
success_message += "Please attach this confirmation message to your submission.\n"
success_message += "\nBelow is a summary of your submission:\n"
success_message += f"- Number of datasets: {num_datasets}\n"
success_message += f"- Number of readme files: {num_readme_files}\n"
success_message += f"- Number of spreadsheet files: {num_spreadsheet_files}\n"
success_message += f"- Total number of subjects: {num_subjects}\n"
success_message += f"- Dataset names: {', '.join(dataset_names)}\n"
success_message += "\nPlease confirm that the information above is correct. If anything seems wrong, please make corrections before submitting.\n"

# Display the summary information to the user
print("\nHere is a summary of your submission:")
print(success_message)

# Ask the user for confirmation before creating the text file
confirm = input("Does the information look correct? (yes/no): ").strip().lower()

# If the user confirms, write the success message to a text file
if confirm == 'yes':
    write_confirmation_file(success_message, folder_path + "Confirmation_Message.txt")
    print(f"Confirmation message saved as 'Confirmation_Message.txt' in {folder_path}.")
else:
    print("Please review your data and make the necessary changes before proceeding.")
