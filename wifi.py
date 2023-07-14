import argparse
import datetime
import os
import time

import pandas as pd
import requests
from prettytable import PrettyTable


def send_request(
    req_headers,
    latrange1,
    latrange2,
    longrange1,
    longrange2,
    location,
    request_delay=5,
    max_retries=3,
):
    """
    Send a request to the Wigle API to search for network data for the specified
    latitude and longitude ranges, and print the results as a pretty table.

    :param req_headers: dict
        The headers to be used in the API request.
    :param latrange1: float
        The lower latitude bound.
    :param latrange2: float
        The upper latitude bound.
    :param longrange1: float
        The lower longitude bound.
    :param longrange2: float
        The upper longitude bound.
    :param location: str
        The name of the location.
    :param request_delay: int, optional
        The number of seconds to wait between API requests.
    :param max_retries: int, optional
        The maximum number of retries on connection errors.
    """
    base_url = "https://api.wigle.net/api/v2/network/search"
    query_params = {
        "latrange1": latrange1,
        "latrange2": latrange2,
        "longrange1": longrange1,
        "longrange2": longrange2,
        "first": 100,
    }

    total_results = []
    current_count = 0
    total_count = None

    print("Retrieving results...")
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(base_url, params=query_params, headers=req_headers)
            status_code = response.status_code

            if status_code == 200:
                data = response.json()
                results = data["results"]
                total_results.extend(results)
                current_count += len(results)

                if total_count is None:
                    total_count = data["totalResults"]

                print(f"Retrieved {current_count} out of {total_count} results")

                if current_count >= total_count:
                    break

                query_params["start"] = current_count
                time.sleep(request_delay)

            elif status_code == 401:
                print("Unauthorized. Check your API token.")
                return

            elif status_code == 429:
                print("Too many requests. Saving the current results.")
                break

            else:
                print(f"Error {status_code}: Failed to retrieve results.")
                return

        except requests.exceptions.ConnectionError:
            print("Connection Error. Retrying...")
            retries += 1
            time.sleep(request_delay)

        except Exception as e:
            print(f"An error occurred: {e}")
            return

    # Save results to a CSV file if there are any results
    if total_results:
        df = pd.DataFrame(total_results)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tests/{location}_{latrange1}_{longrange1}_{timestamp}.csv"
        df.to_csv(
            filename,
            index=False,
            mode="a",
            header=not os.path.isfile(filename),
            escapechar="\\",
        )

        print(f"All results retrieved. Total results: {current_count}")

        # Display results as a pretty table
        print(pretty_table(df))
    else:
        print("No results were retrieved.")


def pretty_table(df):
    """
    Convert a DataFrame into a PrettyTable.

    :param df: pandas.DataFrame
        DataFrame to be converted.
    :return: PrettyTable
        A PrettyTable object containing the data from the DataFrame.
    """
    pt = PrettyTable()
    pt.field_names = df.columns.tolist()

    # Clean non-printable characters
    def clean_string(s):
        return (
            "".join(
                c if c.isprintable() else "?"
                for c in s.encode("ascii", "replace").decode()
            )
            if isinstance(s, str)
            else s
        )

    # Add rows to PrettyTable
    for _, row in df.iterrows():
        pt.add_row([clean_string(item) for item in row])

    return pt


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Request network data for a specified location."
    )
    parser.add_argument(
        "-location",
        choices=["tacoma", "olympia", "seattle"],
        help="Select a location: tacoma, olympia, or seattle.",
    )
    parser.add_argument("-api_token", help="Your API token for Wigle.")

    args = parser.parse_args()

    # Get the API token from the environment variable or the command line argument
    api_token = os.environ.get("WIGLE_API_TOKEN") or args.api_token

    # If API token is not provided through environment variable or argument, prompt user
    if not api_token:
        api_token = input("Please enter your API token for Wigle: ")

    headers = {"Authorization": f"Basic {api_token}"}

    # Latitude and Longitude ranges for specified locations
    location_ranges = {
        "tacoma": {
            "latrange1": 47.2,
            "latrange2": 47.3,
            "longrange1": -122.5,
            "longrange2": -122.4,
        },
        "olympia": {
            "latrange1": 47.0,
            "latrange2": 47.1,
            "longrange1": -122.9,
            "longrange2": -122.8,
        },
        "seattle": {
            "latrange1": 47.6,
            "latrange2": 47.7,
            "longrange1": -122.3,
            "longrange2": -122.2,
        },
    }

    # Get the selected location ranges and send request
    if args.location in location_ranges:
        ranges = location_ranges[args.location]
        send_request(
            headers,
            latrange1=ranges["latrange1"],
            latrange2=ranges["latrange2"],
            longrange1=ranges["longrange1"],
            longrange2=ranges["longrange2"],
            location=args.location,
        )
    else:
        print(
            "Please specify a valid location using -location argument (e.g. -location tacoma)"
        )
