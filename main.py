import os
import subprocess
import sys
import smtp_settings
import gscrap
import valid

def get_script_path(script_name):
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller or cx_Freeze environment
        return os.path.join(sys._MEIPASS, script_name)
    return os.path.join(os.getcwd(), script_name)

def run_scraper():
    script_path = get_script_path('gscrap.py')
    subprocess.run(['python', script_path])

def run_validator():
    script_path = get_script_path('valid.py')
    subprocess.run(['python', script_path])

def set_smtp_settings():
    print("\n--- SMTP Settings ---")
    smtp_settings.SMTP_SERVER = input(f"Enter SMTP Server (current: {smtp_settings.SMTP_SERVER}): ") or smtp_settings.SMTP_SERVER
    smtp_settings.SMTP_PORT = int(input(f"Enter SMTP Port (current: {smtp_settings.SMTP_PORT}): ") or smtp_settings.SMTP_PORT)
    smtp_settings.SMTP_USERNAME = input(f"Enter SMTP Username (current: {smtp_settings.SMTP_USERNAME}): ") or smtp_settings.SMTP_USERNAME
    smtp_settings.SMTP_PASSWORD = input(f"Enter SMTP Password (current: {smtp_settings.SMTP_PASSWORD}): ") or smtp_settings.SMTP_PASSWORD

    with open('smtp_settings.py', 'w') as f:
        f.write(f"SMTP_SERVER = '{smtp_settings.SMTP_SERVER}'\n")
        f.write(f"SMTP_PORT = {smtp_settings.SMTP_PORT}\n")
        f.write(f"SMTP_USERNAME = '{smtp_settings.SMTP_USERNAME}'\n")
        f.write(f"SMTP_PASSWORD = '{smtp_settings.SMTP_PASSWORD}'\n")

    print("\nSMTP settings updated successfully.")

def main():
    print("\033[1mData Spyder Email Suite\033[0m\n")  # Bold welcome text

    while True:
        print("\nMain Menu")
        print("1. Run Email Scraper")
        print("2. Run Email Validator")
        print("3. Set SMTP Settings")
        print("4. Exit")
        choice = input("Please select an option: ")

        if choice == '1':
            run_scraper()
        elif choice == '2':
            run_validator()
        elif choice == '3':
            set_smtp_settings()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
