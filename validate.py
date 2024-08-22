import csv
import smtplib
from email.mime.text import MIMEText

# Load SMTP settings from separate file
with open('smtp_settings.txt', 'r') as f:
    SMTP_SERVER = f.readline().strip()
    SMTP_PORT = int(f.readline().strip())
    SMTP_USERNAME = f.readline().strip()
    SMTP_PASSWORD = f.readline().strip()

def validate_email(email):
    try:
        # Create a text message
        msg = MIMEText('')
        msg['To'] = email
        msg['Subject'] = 'Test Email'

        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        # Try sending the email
        server.sendmail(SMTP_USERNAME, email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error validating {email}: {str(e)}")
        return False

def main():
    # Prompt user to select input CSV file
    input_file = input("Enter the path to the input CSV file: ")

    # Read input CSV file
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        emails = [row[0] for row in reader]

    # Validate emails
    validated_emails = [email for email in emails if validate_email(email)]

    # Save validated emails to separate CSV file
    output_file = input("Enter the path to the output CSV file: ")
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([[email] for email in validated_emails])

if __name__ == "__main__":
    main()