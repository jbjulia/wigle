# WiGLE Network Data Retriever

## Project Description

WiGLE Network Data Retriever is a Python script for querying and retrieving wireless network information within specified geographic areas from the WiGLE database. The WiGLE platform aggregates information on wireless networks (Wi-Fi, cell, Bluetooth) across the globe and provides this data through their API. This script makes use of the WiGLE API to fetch data about wireless networks in specified locations such as Tacoma, Olympia, and Seattle, and presents it in both a human-readable table format and a CSV file.

## Features

- Retrieve wireless network information (such as SSIDs, MAC addresses, signal strength, and geographic coordinates) within specified latitude and longitude ranges.
- Support for querying multiple predefined locations (Tacoma, Olympia, and Seattle) by passing location-specific arguments.
- Handles API rate limiting and pagination to retrieve large datasets.
- Cleans data to remove non-printable characters.
- Outputs the results in a well-formatted table for display in the console.
- Saves the retrieved data to a CSV file for further analysis or processing.
- Ensures that no empty CSV file is saved if no results are retrieved.

## Usage

1. Clone the repository to your local machine.
2. Make sure you have Python 3.x installed. Also, install the required libraries by running `pip install -r requirements.txt`.
3. Set the environment variable `WIGLE_API_TOKEN` with your WiGLE API token, or you can pass it as a command line argument using `-api_token`.
4. Run the script and pass the desired location as an argument. For example, for retrieving data for Tacoma, use:
   ```sh
   python wigle.py -location tacoma
   ```
   Optionally, you can pass your API token through the command line like this:
   ```sh
   python wigle.py -location tacoma -api_token YOUR_API_TOKEN
   ```

## Dependencies

- Python 3.x
- requests
- pandas
- prettytable

## Limitations

- The script is subject to the limitations and quotas of the WiGLE API. Ensure you understand these before running the script extensively.
- The script currently supports only three predefined locations. Custom locations can be added by modifying the script.

## Disclaimer

Please note that accessing or collecting data from wireless networks might have legal and ethical implications. It is essential to ensure that you comply with the laws and regulations of your country or region and respect privacy and data protection rules.