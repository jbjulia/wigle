import argparse
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
    max_retries=3,
    retry_delay=60,
):
    """
    Send a request to the Wigle API to search for network data for the specified
    latitude and longitude ranges and print the results as a pretty table.

    :param req_headers: The headers to be used in the API request.
    :param latrange1: The lower latitude bound.
    :param latrange2: The upper latitude bound.
    :param longrange1: The lower longitude bound.
    :param longrange2: The upper longitude bound.
    :param location: The location of the upper/lower lat/long bound.
    :param max_retries: The maximum number of retries in case of a 429 status code.
    :param retry_delay: The number of seconds to wait before retrying.
    """
    # Set up the initial API query parameters
    query_params = {
        "latrange1": latrange1,
        "latrange2": latrange2,
        "longrange1": longrange1,
        "longrange2": longrange2,
    }

    retries = 0

    while retries < max_retries:
        try:
            # Make the initial API request
            response = requests.get(
                "https://api.wigle.net/api/v2/network/search",
                params=query_params,
                headers=req_headers,
            )

            # Check if the response was successful
            if response.status_code == 200:
                results = response.json()["results"]
                # Convert to DataFrame
                df = pd.DataFrame(results)

                # Convert DataFrame to PrettyTable and print
                print(pretty_table(df))

                # Save the DataFrame to a CSV file with an escape character
                df.to_csv(
                    f"tests/{location}_{latrange1}_{longrange1}.csv",
                    index=False,
                    escapechar="\\",
                )
                return
            elif response.status_code == 429:
                print("Too Many Requests. Waiting before retrying...")
                time.sleep(retry_delay)
                retries += 1
            else:
                print("Error: Received response with status code", response.status_code)
                return
        except Exception as e:
            print("An error occurred:", str(e))
            return


def pretty_table(df):
    """
    Convert a DataFrame into a PrettyTable.

    :param df: DataFrame to be converted.
    :return: A PrettyTable object containing the data from the DataFrame.
    """
    # Create a PrettyTable instance
    pt = PrettyTable()

    # Add columns
    pt.field_names = df.columns.tolist()

    # Function to clean non-printable characters
    def clean_string(s):
        if isinstance(s, str):
            # This removes non-printable characters and replaces non-UTF-8 characters
            return "".join(
                c if c.isprintable() else "?"
                for c in s.encode("ascii", "replace").decode()
            )
        else:
            return s

    # Add rows
    for _, row in df.iterrows():
        cleaned_row = [clean_string(item) for item in row]
        pt.add_row(cleaned_row)

    # Return the PrettyTable
    return pt


def set_environment_variable(name, value):
    """
    Set an environment variable.

    :param name: The name of the environment variable.
    :param value: The value of the environment variable.
    """
    # Setting the environment variable
    os.environ[name] = value


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Request network data for a specified location"
    )
    parser.add_argument(
        "-location", choices=["tacoma", "olympia", "seattle"], help="select location"
    )
    args = parser.parse_args()

    # Set API token as environment variable
    set_environment_variable(
        "WIGLE_API_TOKEN",
        "[ YOUR_API_TOKEN_GOES_HERE ]",
    )

    # Retrieve the API token from environment variable
    api_token = os.environ.get("WIGLE_API_TOKEN")

    # Set headers
    headers = {"Authorization": f"Basic {api_token}"}

    # Send request for the selected location
    if args.location == "tacoma":
        # Tacoma, WA
        send_request(
            headers,
            latrange1=47.2,
            latrange2=47.3,
            longrange1=-122.5,
            longrange2=-122.4,
            location=args.location,
        )
    elif args.location == "olympia":
        # Olympia, WA
        send_request(
            headers,
            latrange1=47.0,
            latrange2=47.1,
            longrange1=-122.9,
            longrange2=-122.8,
            location=args.location,
        )
    elif args.location == "seattle":
        # Seattle, WA
        send_request(
            headers,
            latrange1=47.6,
            latrange2=47.7,
            longrange1=-122.3,
            longrange2=-122.2,
            location=args.location,
        )
    else:
        print(
            "Please specify a valid location using -location argument (e.g. -location tacoma)"
        )
