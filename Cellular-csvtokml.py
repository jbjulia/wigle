import os
import csv

def csv_to_kml(csv_file, kml_file):
    # Open CSV file for reading
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        # Open KML file for writing
        with open(kml_file, 'w') as kmlfile:
            kmlfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            kmlfile.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            kmlfile.write('<Document>\n')
            for row in csvreader:
                # Extract relevant columns
                lat, lon = row['trilat'], row['trilong']
                network_id = row['id']
                # Write Placemark with relevant information
                kmlfile.write('<Placemark>\n')
                kmlfile.write('<name>{}</name>\n'.format(network_id))
                kmlfile.write('<description>ID: {}</description>\n'.format(network_id))
                kmlfile.write('<Point>\n')
                kmlfile.write('<coordinates>{},{},0</coordinates>\n'.format(lon, lat))
                kmlfile.write('</Point>\n')
                kmlfile.write('</Placemark>\n')
            kmlfile.write('</Document>\n')
            kmlfile.write('</kml>\n')

def convert_csv_files_to_kml(input_dir):
    # Iterate over files in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.csv'):
            csv_file = os.path.join(input_dir, file_name)
            kml_file = os.path.join(input_dir, os.path.splitext(file_name)[0] + '.kml')
            csv_to_kml(csv_file, kml_file)

# Specify the directory containing your CSV files
input_directory = r'YOUR DIRECTORY'

convert_csv_files_to_kml(input_directory)