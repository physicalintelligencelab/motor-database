import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

# Abbreviation to standardized name mapping
abbreviation_mapping = {
    "SN": "Subject ID", "TN": "Trial number", "CN": "Condition number", "BN": "Block number", "Cond": "Condition",
    "CCW": "Counterclockwise", "Tgt size": "Target size", "hand_theta": "Hand angle", "hand_theta_maxv": "Hand angle max velocity",
    "hand_theta_maxradv": "Hand angle max radial velocity", "handMaxRadExt": "Maximum radial extension of the hand",
    "hand_theta_50": "Hand angle at 50 miliseconds into the movement", "Raw_ep_hand_ang": "Raw endpoint hand angle",
    "ti": "Target Index", "fbi": "Feeback Index", "ri": "Rotation Index", "clampi": "Clamp Index",
    "MT": "Movement time", "RT": "Reaction time", "ST": "Search time", "radvelmax": "Maximum radial velocity",
    "maxRadDist": "Maximum radial distance", "testMaxRadDist": "Test maximum radial distance", "PB": "Proprioceptive bias",
    "RB": "Rotational bias", "FC_TT": "Feedback Control Task Time", "FC_X": "Feedback Cursor X-coordinate",
    "FC_Y": "Feedback Cursor Y-coordinate", "HL_X": "Hand location X-coordinate", "HL_Y": "Hand location Y-coordinate",
    "FC_bias_X": "Feedback Cursor X-coordinate bias", "FC_bias_Y": "Feedback Cursor Y-coordinate bias",
    "prop_theta": "Proprioceptive Judgement Angle", "MoCA": "Montreal Cognitive Assessment", "UPDRS": "Unified Parkinson's Disease Rating Scale",
    "YOE": "Years of Education", "delayedfb": "Delayed Feedback", "audiodelay": "Audio delay", "tgt_jump": "Target jump",
    "tgt_jump_size": "Target jump size", "tgt_error": "Target error", "Hand_raw": "Raw hand angle",
    "Hand_dt": "Hand displacement time", "Hand_Diff": "Hand difference", "Exp": "Experiment",
    "RT_dt": "Reaction time difference", "Hand_IB": "Hand inter-block", "HRbase": "Hand Report base",
    "FC_TT": "Feedback Control Task Time", "FC_X": "Feedback Control X-coordinate", "FC_Y": "Feedback Control Y-coordinate",
    "StartTime": "Start time", "education": "Education", "technical": "Technical rating",
    "rating": "Enjoyment", "browsertype": "Browser type", "mousetype": "Mouse type", "racialorigin": "Racial origin",
    "repeat": "Number of times participated", "sex": "Sex", "futureemails": "Future emails",
    "NeuroDisease": "Neuro Disease", "NeuroDiseaseDescribe": "Description of disease", "screenheight": "Screen height",
    "screenwidth": "Screen width", "clumsy": "Clumsiness rating", "seedisplay": "Clarity of display",
    "videogames": "Video game experience", "major": "Major", "Sleep": "Daily sleep hours",
    "ComputerUsage": "Computer usage", "gameIndex": "Game index"
}

# Template headers
template_headers = [
    "id", "repeat_number", "researcher_id*", "condition*", "block_number", "trial_number",
    "research_setting*", "hand_or_mouse*", "subject_age", "subject_sex", "subject_race",
    "neuro_condition*", "neuro_description", "years_of_education", "subject_vision",
    "dominant_hand", "screen_height", "screen_width", "device_type", "mouse_type",
    "reaction_time*", "movement_time*", "search_time", "feedback_type*", "feedback_time*",
    "initial_x", "initial_y", "number_of_targets*", "target_type*", "target_angle",
    "target_height", "target_width", "target_x", "target_y", "rotation_angle", "clamp_size",
    "rotation_direction", "hand_angle*", "hand_flip", "hand_base", "hand_max_velocity",
    "cognitive_assessment", "cognitive_assessment_score"
]

def upload_and_update_csvs():
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    if not file_paths:
        return  # If the user cancels the file dialog, return

    try:
        for file_path in file_paths:
            # Process each CSV file
            df = pd.read_csv(file_path)

            # Update column headers based on the abbreviation mapping
            updated_columns = []
            for col in df.columns:
                updated_columns.append(abbreviation_mapping.get(col, col))  # Use the mapped value or the original if not found

            df.columns = updated_columns

            # Replace empty values with "None Provided"
            df.replace("", "None Provided", inplace=True)
            df.fillna("None Provided", inplace=True)

            # Populate the template based on the standardized headers
            populated_template = populate_template(df, template_headers)

            # Replace any remaining empty values with "None Provided"
            populated_template.fillna("None Provided", inplace=True)

            # Save each standardized file as an Excel file
            save_as_excel(populated_template, file_path)

        messagebox.showinfo("Success", "All files have been processed and saved successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to read or process the files: {e}")

# Function to display CSV content
def display_csv(df):
    csv_window = tk.Toplevel(window)
    csv_window.title("Updated CSV Content")
    csv_window.geometry("800x400")
    csv_window.configure(bg="#f0f4f7")

    # Create a treeview widget to display the dataframe
    tree = ttk.Treeview(csv_window)
    tree.pack(expand=True, fill=tk.BOTH)

    # Define the columns
    tree["column"] = list(df.columns)
    tree["show"] = "headings"

    # Set the column headers
    for col in tree["columns"]:
        tree.heading(col, text=col)

    # Add the rows from the dataframe
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

# Function to populate the template with data from the input DataFrame
def populate_template(input_df, template_headers):
    # Initialize a DataFrame with the template headers, filled with "None Provided"
    template_df = pd.DataFrame(columns=template_headers)
    
    # Copy over the matching columns from the input DataFrame
    for col in input_df.columns:
        if col == "Subject ID":  # Map "Subject ID" to "id" in the template
            template_df["id"] = input_df[col]
        elif col in template_df.columns:
            template_df[col] = input_df[col]
        else:
            # If column is not in the template, add it with an asterisk
            template_df[col + "*"] = input_df[col]

    # Replace any remaining empty values with "None Provided"
    template_df.replace("", "None Provided", inplace=True)
    template_df.fillna("None Provided", inplace=True)
    
    return template_df

# Function to save DataFrame as Excel file
def save_as_excel(df, original_file_path):
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")],
                                             initialfile=os.path.splitext(os.path.basename(original_file_path))[0] + "_standardized")
    if save_path:
        try:
            df.to_excel(save_path, index=False)
            messagebox.showinfo("Success", f"File saved successfully as {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

# Main window setup
window = tk.Tk()
window.title("CSV Header Standardizer")
window.geometry("400x200")
window.configure(bg="#f0f4f7")

# Button to upload, update, and save CSV
upload_button = ttk.Button(window, text="Upload, Standardize, and Save as Excel", command=upload_and_update_csvs)
upload_button.pack(pady=20)

# Run the main loop
window.mainloop()
