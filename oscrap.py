import requests
from bs4 import BeautifulSoup
import re
import time
import random
import csv
from twocaptcha import TwoCaptcha

# Initialize 2Captcha solver
solver = TwoCaptcha('5451081542d4e1fdbdbdd1b84cc79cf6')  # Replace with your 2Captcha API key

def solve_recaptcha(sitekey, url):
    try:
        result = solver.recaptcha(
            sitekey=sitekey,
            url=url,
            version='v2'  # or 'v3' based on your CAPTCHA version
        )
        return result['code']
    except Exception as e:
        print(f"Error solving reCAPTCHA: {e}")
        return None

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
    results_per_page = 100
    max_retries = 5

    for page in range(num_pages):
        start = page * results_per_page
        url = f"https://www.google.com/search?q={query}&num={results_per_page}&start={start}"
        retries = 0

        while retries < max_retries:
            try:
                response = requests.get(url, headers=headers)
                
                # Check if response indicates CAPTCHA challenge
                if 'captcha' in response.url:
                    print("CAPTCHA detected. Attempting to solve...")
                    sitekey = '6Ld09CYqAAAAAHc-o4UX2X78IA0PnJG7kF6zTx3I' 
                    captcha_code = solve_recaptcha(sitekey, url)
                    if not captcha_code:
                        print("Failed to solve CAPTCHA.")
                        return emails  # Exit if CAPTCHA solving fails
                
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                snippet_texts = soup.find_all('span', {'class': 'BNeawe s3v9rd AP7Wnd'})
                for snippet in snippet_texts:
                    found_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', snippet.text)
                    emails.extend(found_emails)
                    for email in found_emails:
                        print(f"Found: {email}")
                
                time.sleep(random.uniform(5, 10))  # Increased delay
                break  # Exit retry loop if successful
            
            except requests.exceptions.RequestException as e:
                print(f"Error fetching page {page + 1}: {e}")
                retries += 1
                time.sleep(random.uniform(10, 20))  # Delay before retrying

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
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            for email in emails:
                writer.writerow([email])

        print(f"\nEmails saved to {filename}")
    else:
        print("No emails found.")

if __name__ == "__main__":
    main()
