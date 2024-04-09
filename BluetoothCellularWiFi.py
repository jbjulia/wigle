import os
import re
import time
import pandas as pd
import requests
import datetime

# Constants for API requests
BASE_URL = "https://api.wigle.net/api/v2/"
REQUEST_DELAY = 5
MAX_RETRIES = 3

API_KEY = 'INPUT YOUR API KEY'

def is_valid_token(token):
    """
    Check if a token is valid.

    Parameters:
        token (str): The token to check.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    return bool(re.fullmatch(r"[\w\-_=]*", token))


def get_headers():
    """
    Get the headers with the specific Authorization header.

    Returns:
        dict: The headers with the specific Authorization header.
    """
    return {"Your Authorizaiton Header"}


def send_request(api_type, headers, only_mine, last_updated):
    """
    Send a request to the WiGLE API and save the results.

    Parameters:
        api_type (int): The type of API (0 for Bluetooth, 1 for Cell, 2 for Network).
        headers (dict): The headers to use for the request.
        only_mine (bool): Whether to search only for points discovered by the current user.
        last_updated (str): The last updated time to filter the results.

    Returns:
        None
    """
    api_endpoints = ['bluetooth/search', 'cell/search', 'network/search']
    api_endpoint = api_endpoints[api_type]
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join("output", f"{api_endpoint.split('/')[0]}_{timestamp}.csv")

    current_count = 0
    total_count = None
    retries = 0

    query_params = {
        "onlymine": str(only_mine).lower(),
        "first": 100,
        "lastupdt": last_updated
    }

    print(f"Retrieving results from {BASE_URL + api_endpoint}...")

    # Ensure the output folder exists
    os.makedirs("output", exist_ok=True)

    # Open the file for writing with UTF-8 encoding
    with open(filename, "a", encoding="utf-8") as f:
        while retries < MAX_RETRIES:
            try:
                response = requests.get(BASE_URL + api_endpoint, params=query_params, headers=headers)
                status_code = response.status_code

                if status_code == 200:
                    data = response.json()
                    results = data["results"]
                    current_count += len(results)

                    if total_count is None:
                        total_count = data["totalResults"]

                    print(f"Retrieved {current_count} out of {total_count} results")

                    df = pd.DataFrame(results)
                    df.to_csv(f, index=False, header=f.tell() == 0, escapechar="\\")

                    if current_count >= total_count:
                        break

                    query_params["start"] = current_count
                    time.sleep(REQUEST_DELAY)

                elif status_code == 401:
                    print("Unauthorized. Check your API key.")
                    break

                elif status_code == 429:
                    print("Too many requests. Saving the current results.")
                    break

                else:
                    print(f"Error {status_code}: Failed to retrieve results.")
                    break

            except requests.exceptions.Timeout:
                print("Request timed out. Retrying...")
                retries += 1
                time.sleep(REQUEST_DELAY)

            except requests.exceptions.TooManyRedirects:
                print("Too many redirects. Terminating request.")
                break

            except requests.exceptions.ConnectionError:
                print("Connection Error. Retrying...")
                retries += 1
                time.sleep(REQUEST_DELAY)

            except Exception as e:
                print(f"An error occurred: {e}")
                break

        print(f"All results retrieved from {BASE_URL + api_endpoint}. Total results: {current_count}")


def main():
    """
    Get the API type, last updated time, and other parameters from the user,
    and send a request to the WiGLE API.

    Returns:
        None
    """
    api_type = int(input("Enter the API type (0 for Bluetooth, 1 for Cell, 2 for Network): "))
    only_mine = input("Search only for points first discovered by the current user? (true/false): ").lower() == "true"
    last_updated = input("Enter the last updated time (yyyyMMdd[hhmm[ss]]): ")
    headers = get_headers()

    send_request(api_type, headers, only_mine, last_updated)


if __name__ == "__main__":
    main()
