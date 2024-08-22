import re
import urllib.request
import time
import os
from datetime import datetime
from bs4 import BeautifulSoup

# Regular expression to match email addresses
emailRegex = re.compile(r'''
(
    [a-zA-Z0-9_.+]+   # username
    @
    [a-zA-Z0-9_.+]+   # domain name
)
''', re.VERBOSE)

# Function to extract emails from text
def extractEmailsFromUrlText(urlText, emailFile):
    extractedEmails = emailRegex.findall(urlText)
    uniqueEmails = set(extractedEmails)
    lenh = len(uniqueEmails)
    print("\tNumber of Emails : %s\n" % lenh)
    for email in uniqueEmails:
        emailFile.write(email + "\n")  # Save emails to file

# Function to read HTML content of a webpage
def htmlPageRead(url, i, emailFile):
    try:
        start = time.time()
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        urlHtmlPageRead = response.read()
        urlText = urlHtmlPageRead.decode()
        print("%s.%s\tFetched in : %s" % (i, url, (time.time() - start)))
        extractEmailsFromUrlText(urlText, emailFile)
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")

# Function to handle crawling and extracting emails
def emailsLeechFunc(url, i, emailFile):
    try:
        # Read the search result page
        start = time.time()
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        urlHtmlPageRead = response.read()
        soup = BeautifulSoup(urlHtmlPageRead, 'html.parser')

        # Find all links in the search result page
        links = [a['href'] for a in soup.find_all('a', href=True) if 'url?q=' in a['href']]

        for link in links:
            # Extract actual URL from the search result link
            actual_url = link.split('url?q=')[1].split('&')[0]
            htmlPageRead(actual_url, i, emailFile)
    except Exception as e:
        print(f"Error processing search result page {url}: {e}")

# Main execution function
def main():
    # Get user input
    email_provider = input("Enter the email provider (e.g., gmail.com): ")
    keyword = input("Enter the keyword (e.g., trucking): ")
    location = input("Enter the location (e.g., Canada): ")

    # Create Google search query URL
    search_query = f'"@{email_provider}" "{keyword}" "{location}"'
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"

    # Generate a timestamp for the email file name
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    email_filename = f"emails{timestamp}.txt"

    # Open the email file for writing
    with open(email_filename, 'a') as emailFile:
        print(f"Fetching emails for search URL: {search_url}")
        emailsLeechFunc(search_url, 1, emailFile)
        print(f"Emails saved to {email_filename}")

# Run the script
if __name__ == "__main__":
    main()
