import requests


# Constants
API_URL = "https://thecannon.ca"


def main():
    response = requests.get(f"{API_URL}/housing")
    if response.ok:
        print(response.text)
    else:
        print(f"Failed to retrieve data: {response.status_code}")


if __name__ == "__main__":
    main()
