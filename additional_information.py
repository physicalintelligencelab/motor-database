import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import csv
import subprocess

# Function to hash email addresses for anonymization
def hash_email(email):
    return hashlib.sha256(email.encode()).hexdigest()

# Function to handle project type selection
def on_project_type_change(event):
    # Clear all entry fields
    for var in [title_var, authors_var, date_var, citation_var, doi_var, journal_var, country_var, description_var, additional_comments_var, email_var]:
        var.set("")

    # Hide all fields initially
    for widget in widgets_to_hide:
        widget.grid_remove()

    # Display relevant fields based on project type
    project_type = project_type_var.get()

    common_widgets = [title_label, title_entry, authors_label, authors_entry, date_label, date_entry]
    for widget in common_widgets:
        widget.grid(padx=10, pady=5, sticky="w")

    if project_type in ["preprint", "published research paper"]:
        citation_label.grid(padx=10, pady=5, sticky="w")
        citation_entry.grid(padx=10, pady=5, sticky="w")
        doi_label.grid(padx=10, pady=5, sticky="w")
        doi_entry.grid(padx=10, pady=5, sticky="w")
        country_label.grid(padx=10, pady=5, sticky="w")
        country_entry.grid(padx=10, pady=5, sticky="w")

        if project_type == "published research paper":
            journal_label.grid(padx=10, pady=5, sticky="w")
            journal_entry.grid(padx=10, pady=5, sticky="w")
    
    elif project_type in ["under_review", "unsubmitted", "rejected"]:
        description_label.grid(padx=10, pady=5, sticky="w")
        description_entry.grid(padx=10, pady=5, sticky="w")

    additional_comments_label.grid(padx=10, pady=5, sticky="w")
    additional_comments_entry.grid(padx=10, pady=5, sticky="w")
    email_label.grid(padx=10, pady=5, sticky="w")
    email_entry.grid(padx=10, pady=5, sticky="w")

# Function to save data and run upload_csv.py
def save_data():
    project_type = project_type_var.get()
    title = title_var.get()
    authors = authors_var.get()
    date = date_var.get()
    additional_comments = additional_comments_var.get()
    email = email_var.get()

    if project_type in ["preprint", "published research paper"]:
        citation = citation_var.get()
        doi = doi_var.get()
        country = country_var.get()
        journal = journal_var.get() if project_type == "published research paper" else ""
        description = ""
    else:
        citation = ""
        doi = ""
        journal = ""
        country = ""
        description = description_var.get()

    hashed_email = hash_email(email)

    # Compile data
    data = [project_type, title, authors, citation, doi, date, journal, country, description, additional_comments, hashed_email]
    headers = ["Project Type", "Title", "Authors", "Citation", "DOI", "Date", "Journal", "Country", "Description", "Additional Comments", "Hashed Email"]

    # Confirm information
    confirmation_message = f"Please confirm the following information:\n\n"
    for header, value in zip(headers, data):
        confirmation_message += f"{header}: {value}\n"

    confirm = messagebox.askyesno("Confirm Information", confirmation_message)
    if confirm:
        # Write to CSV file
        file_name = "projects.csv"
        with open(file_name, mode="a", newline="") as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # If the file is empty, write headers
                writer.writerow(headers)
            writer.writerow(data)
        
        # Run upload_csv.py
        try:
            subprocess.run(["python", "upload_csv.py"], check=True)
            messagebox.showinfo("Success", "Data saved and upload_csv.py ran successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to run upload_csv.py: {e}")
        
        window.quit()
    else:
        edit_fields()

# Function to allow editing of fields
def edit_fields():
    messagebox.showinfo("Edit", "Please edit the values and confirm again.")

# Create the GUI window
window = tk.Tk()
window.title("Project Submission")
window.geometry("500x600")  # Set window size
window.configure(bg="#f0f4f7")  # Background color

# Define a style
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), background="#f0f4f7")
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12), background="#007BFF", foreground="#ffffff", padding=6)

# Project Type Dropdown
project_type_var = tk.StringVar()
ttk.Label(window, text="Select Project Type:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
project_type_menu = ttk.Combobox(window, textvariable=project_type_var, font=("Helvetica", 12))
project_type_menu['values'] = ("under_review", "published research paper", "preprint", "unsubmitted", "rejected")
project_type_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")
project_type_menu.bind("<<ComboboxSelected>>", on_project_type_change)

# Title of Project
title_var = tk.StringVar()
title_label = ttk.Label(window, text="Title of Project")
title_entry = ttk.Entry(window, textvariable=title_var, width=40)

# Authors
authors_var = tk.StringVar()
authors_label = ttk.Label(window, text="Authors")
authors_entry = ttk.Entry(window, textvariable=authors_var, width=40)

# Date
date_var = tk.StringVar()
date_label = ttk.Label(window, text="Date")
date_entry = ttk.Entry(window, textvariable=date_var, width=40)

# Citation
citation_var = tk.StringVar()
citation_label = ttk.Label(window, text="Citation (DOI)")
citation_entry = ttk.Entry(window, textvariable=citation_var, width=40)

# DOI
doi_var = tk.StringVar()
doi_label = ttk.Label(window, text="DOI")
doi_entry = ttk.Entry(window, textvariable=doi_var, width=40)

# Journal (if published)
journal_var = tk.StringVar()
journal_label = ttk.Label(window, text="Journal")
journal_entry = ttk.Entry(window, textvariable=journal_var, width=40)

# Country
country_var = tk.StringVar()
country_label = ttk.Label(window, text="Country")
country_entry = ttk.Entry(window, textvariable=country_var, width=40)

# Description/Abstract (for non-published)
description_var = tk.StringVar()
description_label = ttk.Label(window, text="Text description of project")
description_entry = ttk.Entry(window, textvariable=description_var, width=40)

# Additional Comments
additional_comments_var = tk.StringVar()
additional_comments_label = ttk.Label(window, text="Additional Comments")
additional_comments_entry = ttk.Entry(window, textvariable=additional_comments_var, width=40)

# Email
email_var = tk.StringVar()
email_label = ttk.Label(window, text="Email of Uploader for Contact")
email_entry = ttk.Entry(window, textvariable=email_var, width=40)

# Store widgets to hide and show
widgets_to_hide = [title_label, title_entry, authors_label, authors_entry, date_label, date_entry, citation_label, citation_entry,
                   doi_label, doi_entry, journal_label, journal_entry, country_label, country_entry, description_label, description_entry,
                   additional_comments_label, additional_comments_entry, email_label, email_entry]

# Submit Button
submit_button = ttk.Button(window, text="Submit", command=save_data)
submit_button.grid(row=20, columnspan=2, padx=10, pady=20)

# Run the GUI loop
window.mainloop()
