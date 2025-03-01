import requests 
import os
import csv
from io import StringIO
from datetime import datetime

url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2023-01-01&endtime=2023-01-02'

def import_data(url):   
    response = requests.get(url)
    response.raise_for_status()
    data_text = response.text
    
    os.makedirs('data', exist_ok=True)
    
    file_path = os.path.join('data', 'dataset_M3.txt')
    
    with open(file_path, "w+", encoding="utf-8") as f:
        f.write(data_text)
        f.seek(0)
        return f.readlines()


#import_data(url)

data_list = import_data(url)


def clean_data(data_list):
    data_string = ''.join(data_list)
    csv_reader = csv.reader(StringIO(data_string))
    
    header_row = next(csv_reader)
    date_index = header_row.index('time')
    cleaned_rows = [header_row]
    
    for row in csv_reader:
        try:
            og_date = row[date_index].rstrip('Z')
            dt = datetime.fromisoformat(og_date)
            row[date_index] = dt.strftime('%d-%m-%Y %H:%M:%S')
        except Exception as e:
            print(f'There was an error processing row {e}')
        cleaned_rows.append(row)
        
        
    os.makedirs('output', exist_ok=True)
    output_file = os.path.join('output', 'cleaned_data_M3.txt')
    
    with open(output_file, 'w', newline= '', encoding= 'utf-8') as f:
        csv.writer(f).writerows(cleaned_rows)
    
    cleaned_text= [','.join(row) + '\n' for row in cleaned_rows]
    
    return cleaned_text

#clean_data(data_list)