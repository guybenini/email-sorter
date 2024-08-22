import re
import os
from tkinter import Tk, filedialog
from datetime import datetime

# Function to validate email format
def is_valid_email(email):
    pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    return pattern.match(email) is not None

# Function to check if an email is too long
def is_too_long(email, max_length=254):
    return len(email) > max_length

# Function to check if an email contains ellipses
def contains_ellipsis(email):
    return '...' in email

# Function to remove duplicates and malformed emails
def clean_email_list(email_list):
    cleaned_emails = set()
    for email in email_list:
        email = email.strip()
        if is_valid_email(email) and not is_too_long(email) and not contains_ellipsis(email):
            cleaned_emails.add(email)
    return cleaned_emails

# Function to save cleaned emails to a file
def save_cleaned_emails(cleaned_emails):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"cleaned_emails_{timestamp}.txt")
    
    with open(output_file, "w") as f:
        for email in cleaned_emails:
            f.write(f"{email}\n")
    
    print(f"Cleaned email list saved to: {output_file}")

# Function to load emails from a file
def load_email_list(file_path):
    with open(file_path, "r") as file:
        email_list = file.readlines()
    return email_list

# Main function to run the script
def main():
    # Prompt user to select the file containing email list
    Tk().withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename(title="Select Email List File",
                                           filetypes=(("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")))
    
    if file_path:
        email_list = load_email_list(file_path)
        cleaned_emails = clean_email_list(email_list)
        save_cleaned_emails(cleaned_emails)
    else:
        print("No file selected. Exiting...")

if __name__ == "__main__":
    main()
