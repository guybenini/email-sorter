import re
import urllib.request
import time
import os
from datetime import datetime
from bs4 import BeautifulSoup

# Improved regular expression to match valid email addresses more accurately
emailRegex = re.compile(r'''
(
    [a-zA-Z0-9._%+-]+      # username
    @
    [a-zA-Z0-9.-]+        # domain name
    \.[a-zA-Z]{2,}        # top-level domain
)
''', re.VERBOSE)

# Function to validate emails and reject those with .png extension
def is_valid_email(email):
    # Additional validation for email structure and domain
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        domain = email.split('@')[1]
        # Check if the domain has at least one dot and is not too short
        if domain.count('.') >= 1 and len(domain.split('.')[0]) > 1:
            # Reject emails with .png extension
            if not email.lower().endswith('.png'):
                return True
    return False

# Function to extract emails from text
def extractEmailsFromUrlText(urlText, seenEmails):
    extractedEmails = emailRegex.findall(urlText)
    validEmails = {email for email in extractedEmails if is_valid_email(email)}
    newEmails = validEmails - seenEmails
    seenEmails.update(newEmails)
    
    return newEmails

# Function to read HTML content of a webpage
def htmlPageRead(url, i, seenEmails):
    try:
        start = time.time()
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        urlHtmlPageRead = response.read()
        urlText = urlHtmlPageRead.decode()
        print("%s.%s\tFetched in : %s" % (i, url, (time.time() - start)))
        return extractEmailsFromUrlText(urlText, seenEmails)
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return set()

# Function to handle crawling and extracting emails
def emailsLeechFunc(url, i, seenEmails, target_email_count):
    total_emails_extracted = set()
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        urlHtmlPageRead = response.read()
        soup = BeautifulSoup(urlHtmlPageRead, 'html.parser')

        # Find all links in the search result page
        links = [a['href'] for a in soup.find_all('a', href=True) if 'url?q=' in a['href']]

        for link in links:
            if len(total_emails_extracted) >= target_email_count:
                break

            actual_url = link.split('url?q=')[1].split('&')[0]
            newEmails = htmlPageRead(actual_url, i, seenEmails)
            total_emails_extracted.update(newEmails)
    except Exception as e:
        print(f"Error processing search result page {url}: {e}")
    
    return total_emails_extracted

# Main execution function
def main():
    # Get user input
    email_provider = input("Enter the email provider (e.g., gmail.com): ")
    keyword = input("Enter the keyword (e.g., CEO): ")
    location = input("Enter the location (e.g., London): ")
    target_email_count = int(input("Enter the number of emails you want to extract: "))

    # Create Google search query URL with 100 results per page
    search_query = f'"@{email_provider}" "{keyword}" "{location}"'
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}&num=100"

    # Generate a timestamp for the email file name
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    email_filename = f"emails{timestamp}.txt"

    seenEmails = set()
    total_emails_extracted = set()
    page_number = 1

    try:
        with open(email_filename, 'a') as emailFile:
            while len(total_emails_extracted) < target_email_count:
                paginated_search_url = f"{search_url}&start={(page_number - 1) * 100}"
                print(f"Fetching emails for page {page_number}...")
                newEmails = emailsLeechFunc(paginated_search_url, page_number, seenEmails, target_email_count - len(total_emails_extracted))
                total_emails_extracted.update(newEmails)

                # Save progress after each page is processed
                for email in newEmails:
                    emailFile.write(email + "\n")

                print(f"Total emails extracted so far: {len(total_emails_extracted)}")
                page_number += 1

                if len(newEmails) == 0:
                    print("No more emails found. Stopping the search.")
                    break
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        # Save the results before stopping
        with open(email_filename, 'a') as emailFile:
            for email in total_emails_extracted:
                emailFile.write(email + "\n")
        print(f"Emails saved to {email_filename}. Total emails extracted: {len(total_emails_extracted)}")

# Run the script
if __name__ == "__main__":
    main()
