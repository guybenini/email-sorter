from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

def main():
    mail_provider = input("Enter the mail provider (e.g., gmail.com) or press Enter to include all providers: ").strip()
    keyword = input("Enter the keyword (e.g., CEO): ").strip()
    location = input("Enter the location (e.g., London): ").strip()
    num_emails = int(input("How many emails do you want to extract? "))

    # Adjust the search query based on whether a mail provider was given
    if mail_provider:
        search_query = f'"@{mail_provider}" "{keyword}" "{location}"'
    else:
        search_query = f'"{keyword}" "{location}" email'

    # Set up WebDriver
    driver = webdriver.Chrome()
    driver.get('https://www.google.com')

    # Find the search box, enter the query, and hit return
    search_box = driver.find_element("name", "q")
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    emails = []
    for _ in range(num_emails // 10):
        time.sleep(2)  # Wait for the page to load
        snippets = driver.find_elements("xpath", "//span[@class='BNeawe']")

        for snippet in snippets:
            snippet_text = snippet.text
            found_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', snippet_text)
            emails.extend(found_emails)

        if len(emails) >= num_emails:
            break

        # Click on the "Next" button to go to the next page of results
        try:
            next_button = driver.find_element("xpath", "//a[@id='pnnext']")
            next_button.click()
        except:
            print("No more pages or an error occurred.")
            break

    driver.quit()

    emails = emails[:num_emails]
    print(f"\nExtracted {len(emails)} emails:\n")
    for email in emails:
        print(email)

    with open("output.csv", "w") as f:
        for email in emails:
            f.write(f"{email}\n")

    print("\nEmails saved to output.csv")

if __name__ == "__main__":
    main()
