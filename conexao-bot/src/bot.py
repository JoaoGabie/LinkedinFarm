from config.try_login import try_login
from config.linkedin_search import LinkedInSearch
from playwright.sync_api import sync_playwright

def main():
    # Manage the Playwright instance in a single with block
    with sync_playwright() as p:
        # Attempt to log in and get the page and browser objects
        success, page, browser = try_login(p)

        # Check if login was successful
        if success:
            print("Login attempt: Success")

            # Initialize the LinkedInSearch class and set search keywords
            search = LinkedInSearch("tech recruiter", "1")
            search_url = search.get_url()
            print(f"Navigating to search URL: {search_url}")

            # Navigate to the search URL using the page object
            page.goto(search_url)
            page.wait_for_load_state("networkidle")

            # Example: Print the page title
            title = page.title()
            print(f"Page title: {title}")

            # Clean up by closing the browser
            browser.close()
        else:
            print("Login attempt: Failure")

if __name__ == "__main__":
    main()