# WiGLE Network Data Retriever

## Project Description

WiGLE Network Data Retriever is a Python script for querying and retrieving wireless network information within specified geographic areas from the WiGLE database. The WiGLE platform aggregates information on wireless networks (Wi-Fi, Cellular, Bluetooth) across the globe and provides this data through their API. This script makes use of the WiGLE API to fetch data about wireless networks in specific latitude and longitude ranges and stores this data in a CSV file for further analysis.

## Features

- Retrieve wireless network information (such as SSIDs, MAC addresses, signal strength, and geographic coordinates) within specified latitude and longitude ranges.
- Handles API rate limiting and pagination to retrieve large datasets.
- Supports input validation for geographic coordinates and API tokens.
- Safely handles interruptions during data retrieval, ensuring that retrieved data is not lost.
- Outputs the progress of data retrieval in the console.
- Saves the retrieved data to a CSV file for further analysis or processing.
- CSV file names are timestamped for easy identification of different data retrieval sessions.
- Manages error scenarios during the request phase including timeouts, redirects, and unauthorized access, providing relevant feedback.

## Usage

1. Clone the repository to your local machine.
2. Make sure you have Python 3.x installed. Also, install the required libraries by running `pip install -r requirements.txt`.
3. Run the script. When prompted, enter the desired latitude and longitude ranges and your WiGLE API token.

   ```sh
   python wigle.py
   ```

   For instance, if you want to collect data in the geographic region defined by the latitude range 47.2 to 47.3 and the longitude range -122.5 to -122.4, and your API token is `YOUR_API_TOKEN`, you would do:

   ```sh
   python wigle.py
   Enter lower latitude: 47.2
   Enter upper latitude: 47.3
   Enter lower longitude: -122.5
   Enter upper longitude: -122.4
   Enter your API token: YOUR_API_TOKEN
   ```

   The script will then start retrieving data and save it to a CSV file in the `tests` folder. The file will be named according to the first latitude and longitude in your range, along with the current timestamp.

   You can stop the script at any time by pressing `Ctrl+C`. The script will save the data retrieved so far to the CSV file.

## Dependencies

- Python 3.x
- requests
- pandas

## Limitations

- The script is subject to the limitations and quotas of the WiGLE API. Ensure you understand these before running the script extensively.
- The retrieval process can take a long time if the specified geographic range is large.
- There is a maximum of 3 retries for the failed requests.

## Disclaimer

Please note that accessing or collecting data from wireless networks might have legal and ethical implications. It is essential to ensure that you comply with the laws and regulations of your country or region and respect privacy and data protection rules.

## Authors

[Joseph Julian](https://github.com/jbjulia)  
[D14b0l1c](https://github.com/D14b0l1c)