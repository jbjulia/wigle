import datetime
import os
import re
import time

import pandas as pd
import requests

# Constants for coordinate validation
MIN_LATITUDE, MAX_LATITUDE = -90, 90
MIN_LONGITUDE, MAX_LONGITUDE = -180, 180

# Constants for API requests
BASE_URL = "https://api.wigle.net/api/v2/bluetooth/search"
REQUEST_DELAY = 5
MAX_RETRIES = 3


def is_valid_token(token):
    """
    Check if a token is valid.

    Parameters:
        token (str): The token to check.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    return bool(re.fullmatch(r"[\w\-_=]*", token))


def get_input(prompt, validation_func):
    """
    Get validated user input.

    Parameters:
        prompt (str): The input prompt to display.
        validation_func (function): The validation function to use on the input.

    Returns:
        str: The user input if it is valid.
    """
    while True:
        value = input(prompt).strip()
        if validation_func(value):
            return value
        print("Invalid input. Please try again.")


def get_coordinate(prompt, min_val, max_val):
    """
    Get a coordinate from the user.

    Parameters:
        prompt (str): The input prompt to display.
        min_val (float): The minimum valid value for the coordinate.
        max_val (float): The maximum valid value for the coordinate.

    Returns:
        float: The coordinate if it is valid.
    """
    while True:
        value = input(prompt)
        try:
            value = float(value)
            if min_val <= value <= max_val:
                return value
            else:
                print(
                    f"Invalid input. Value should be between {min_val} and {max_val}."
                )
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_coordinate_range(lower_prompt, upper_prompt, min_val, max_val):
    """
    Get a coordinate range from the user.

    Parameters:
        lower_prompt (str): The input prompt for the lower value of the range.
        upper_prompt (str): The input prompt for the upper value of the range.
        min_val (float): The minimum valid value for the coordinate.
        max_val (float): The maximum valid value for the coordinate.

    Returns:
        tuple: The coordinate range if it is valid.
    """
    while True:
        lower = get_coordinate(lower_prompt, min_val, max_val)
        upper = get_coordinate(upper_prompt, min_val, max_val)
        if lower < upper:
            return lower, upper
        print("Invalid range. The lower value should be less than the upper value.")


def get_token(prompt):
    """
    Get an API token from the user.

    Parameters:
        prompt (str): The input prompt to display.

    Returns:
        dict: The Authorization header if the token is valid.
    """
    token = get_input(prompt, is_valid_token)
    return {"Authorization": f"Basic {token}"}


def send_request(headers, latrange1, latrange2, longrange1, longrange2):
    """
    Send a request to the WiGLE API and save the results.

    Parameters:
        headers (dict): The headers to use for the request.
        latrange1 (float): The lower latitude of the range to request.
        latrange2 (float): The upper latitude of the range to request.
        longrange1 (float): The lower longitude of the range to request.
        longrange2 (float): The upper longitude of the range to request.

    Returns:
        None
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join("tests", f"{latrange1}_{longrange1}_{timestamp}.csv")

    current_count = 0
    total_count = None
    retries = 0

    query_params = {
        "latrange1": latrange1,
        "latrange2": latrange2,
        "longrange1": longrange1,
        "longrange2": longrange2,
        "first": 100,
    }

    print("Retrieving results...")

    with open(filename, "a") as f:
        while retries < MAX_RETRIES:
            try:
                response = requests.get(BASE_URL, params=query_params, headers=headers)
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
                    print("Unauthorized. Check your API token.")
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

        print(f"All results retrieved. Total results: {current_count}")


def main():
    """
    Get the latitude and longitude ranges and API token from the user,
    and send a request to the WiGLE API.

    Returns:
        None
    """
    lat_range_1, lat_range_2 = get_coordinate_range(
        "Enter lower latitude: ", "Enter upper latitude: ", MIN_LATITUDE, MAX_LATITUDE
    )
    long_range_1, long_range_2 = get_coordinate_range(
        "Enter lower longitude: ",
        "Enter upper longitude: ",
        MIN_LONGITUDE,
        MAX_LONGITUDE,
    )
    headers = get_token("Enter your API token: ")

    send_request(headers, lat_range_1, lat_range_2, long_range_1, long_range_2)


if __name__ == "__main__":
    main()