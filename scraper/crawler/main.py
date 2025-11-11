import requests
from bs4 import BeautifulSoup as bs4

# Constants
API_URL = "https://thecannon.ca"
HEADERS = {
    "Content-Type": "text/html",
    "Accept": "text/html",
}


def get_housing_info() -> dict:
    page = 1
    housing_links = {}

    while True:
        print(f"Fetching page: {page}")
        response = requests.get(f"{API_URL}/housing/page/{page}", headers=HEADERS)
        if not response.ok:
            print(f"Error: Unable to fetch the housing page on page {page}")
            return {}

        html = bs4(response.text, "html.parser")
        links = html.select(f'a[href^="{API_URL}/classified/housing"]')

        # If no housing links are found, break the loop!
        if not links:
            break

        for link in links:
            print(f"Found housing link: {link['href']}")
            posting_response = requests.get(link["href"], headers=HEADERS)
            if not posting_response.ok:
                print(f"Error: Unable to fetch the posting at {link['href']}")
                continue

            posting_html = bs4(posting_response.text, "html.parser").prettify()
            housing_links[link["href"]] = posting_html

        requests.get(f"{API_URL}/classified/housing/page/{page}")
        page += 1

    return housing_links


def main():
    housing_info = get_housing_info()
    if not housing_info:
        print("No housing information found")
        return

    print("Housing information found:")
    with open("housing_info.html", "w", encoding="utf-8") as f:
        for link, html in housing_info.items():
            f.write(f"<!-- Link: {link} -->\n")
            f.write(html + "\n\n")


if __name__ == "__main__":
    main()
