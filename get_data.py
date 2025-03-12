import dotenv
import os
import requests
import gzip
import io
import csv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

class METAR:
    
    def __init__(self):
        self.base_url = os.getenv("AVIATION_WEATHER_BASE_URL")
        self.data=[]

    def get_all_metar_gzip(self):
        query_url = "/data/cache/metars.cache.csv.gz"
        response = requests.get(self.base_url + query_url)
        
        if response.status_code == 200:
            with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as gz:
                with io.TextIOWrapper(gz, encoding='utf-8') as reader:
                    # Skip the first 5 lines
                    for _ in range(5):
                        next(reader)
                    
                    # Use the 6th line as the header
                    header = next(reader).strip().split(',')
                    
                    # Initialize the DictReader with the header
                    csv_reader = csv.DictReader(reader, fieldnames=header)
                    
                    # Process each row as needed
                    for row in csv_reader:
                        self.data.append(row)
        else:
            raise Exception(f"Failed to download file: {response.status_code}")

