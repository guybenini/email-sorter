import requests
from bs4 import BeautifulSoup
import re
import time
import random

def get_search_results(query, num_pages):
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ])
    }
    emails = []
    results_per_page = 10  # Set the number of results per page to 10

    for page in range(num_pages):
        start = page * results_per_page
        url = f"https://www.google.com/search?q={query}&num={results_per_page}&start={start}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extracting emails from the search result snippets
            snippet_texts = soup.find_all('span', {'class': 'BNeawe s3v9rd AP7Wnd'})
            for snippet in snippet_texts:
                found_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', snippet.text)
                emails.extend(found_emails)
                for email in found_emails:
                    print(f"Found: {email}")
            
            time.sleep(random.uniform(2, 5))  # Increase the random delay to avoid being detected as a bot
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve page {page + 1}: {e}")
            time.sleep(random.uniform(10, 20))  # Longer delay on failure to reduce chance of being blocked
    
    return list(set(emails))

def main():
    top_email_providers = [
        "gmail.com", "outlook.com", "yahoo.com", "icloud.com", "aol.com",
        "protonmail.com", "zoho.com", "mail.com", "gmx.com", "yandex.com",
        "fastmail.com", "tutanota.com", "gmx.de", "rediffmail.com", "web.de",
        "lycos.com", "bluemail.net", "zoho.com", "hushmail.com", "runbox.com"
    ]

    mail_provider = input("Enter the mail provider (e.g., gmail.com) or press Enter to search all top providers: ").strip()
    keyword = input("Enter the keyword (e.g., CEO): ").strip()
    location = input("Enter the location (e.g., London): ").strip()
    num_emails = int(input("How many emails do you want to extract? "))

    search_queries = []
    if mail_provider:
        search_queries.append(f'"@{mail_provider}" "{keyword}" "{location}"')
    else:
        for provider in top_email_providers:
            search_queries.append(f'"@{provider}" "{keyword}" "{location}"')

    emails = []
    for query in search_queries:
        print(f"\nSearching for: {query}\n")
        # Calculate the number of pages needed to collect the desired number of emails
        results_per_page = 10
        num_pages = (num_emails // results_per_page) + 1

        emails.extend(get_search_results(query, num_pages=num_pages))

        if len(emails) >= num_emails:
            break

    if emails:
        emails = emails[:num_emails]
        print(f"\nExtracted {len(emails)} emails:\n")
        for email in emails:
            print(email)

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"output_{timestamp}.csv"
        with open(filename, "w") as f:
            for email in emails:
                f.write(f"{email}\n")

        print(f"\nEmails saved to {filename}")
    else:
        print("No emails found.")

if __name__ == "__main__":
    main()
