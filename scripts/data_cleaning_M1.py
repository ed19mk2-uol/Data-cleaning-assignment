# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
import requests
import os
from datetime import datetime
import pandas as pd

def import_data(url):
    os.makedirs('data', exist_ok=True)#creates the data folder if it already exists ignore
    file_name = 'dataset_M1.txt'#file name
    file_path = os.path.join('data', file_name)#path for the file
    response = requests.get(url)#get the url
    if response.status_code == 200:  #if the url request was sucessful
        with open(file_path, 'w') as file:  # Open the file in write mode
            file.write(response.text)  # Write the content to the file

        with open(file_path, 'r') as file:  # Open the file in read mode
            lines = file.readlines()  # Read all lines into a list
        return lines#returns them

def clean_data(data_lines):
    os.makedirs('output', exist_ok=True)#creates output folder if it already exists ignore
    cleaned_file_name = 'cleaned_data_M1.txt'#file name
    cleaned_file_path = os.path.join('output', cleaned_file_name)#path for the file
    with open(cleaned_file_path, 'w') as cleaned_file:#opens file in write mode
        for line in data_lines[1:]:#for ignoring headers
            columns = line.strip().split(',')#removes any whitespace and seperates it into columns
            timestamp = columns[0]#first coloumn

            try:#this is to skip any errors
                dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")#matches the current time format
                formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")#converts it in to the format we need
                print(f"Original: {timestamp} -> Formatted: {formatted_time}")#fancy way of printing old and new

                cleaned_file.write(formatted_time + '\n')#writes the formatted time with a new line
            except ValueError:
                print(f"Skipping invalid timestamp: {timestamp}")#this skips any invalid lines
                continue#continues the loop


url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2023-01-01&endtime=2023-12-31&minmagnitude=5"


data_lines = import_data(url)#input

if data_lines:
    clean_data(data_lines)#output

# +
import requests
import os
from datetime import datetime

def import_data(url):
    os.makedirs('data', exist_ok=True) #creates data folder if it already exists ignore
    file_name = 'dataset_M1.txt'#name of the file
    file_path = os.path.join('data', file_name)#path for the file download
    response = requests.get(url)#get url
    if response.status_code == 200:#check if it was sucessful
        with open(file_path, 'w') as file:#Opens file in write mode
            file.write(response.text)#writes the content to the file

        with open(file_path, 'r') as file:#opens the file in read mode
            lines = file.readlines()#stores them as strings
        return lines

url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2023-01-01&endtime=2023-12-31&minmagnitude=5"
lines = import_data(url)  

def clean_data(data_text_list):
    os.makedirs('output', exist_ok=True)  # Creates output folder if it doesn't exist
    cleaned_file_name = 'cleaned_data_M1.txt'  # Name of the cleaned data file
    cleaned_file_path = os.path.join('output', cleaned_file_name)  # Path for the cleaned file

    # Convert the data list to a DataFrame
    from io import StringIO
    raw_data = '\n'.join(data_text_list)
    df = pd.read_csv(StringIO(raw_data))

    # Ensure the time column is processed correctly
    df['time'] = pd.to_datetime(df['time'], format="%Y-%m-%dT%H:%M:%S.%fZ", errors='coerce')

    # Filter for the valid date range
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 2)
    df_filtered = df[(df['time'] >= start_date) & (df['time'] <= end_date)]

    # Format the time column to the desired format
    cleaned_times = df_filtered['time'].dt.strftime("%Y-%m-%d %H:%M:%S").tolist()

    # Save cleaned data to the new file
    with open(cleaned_file_path, 'w') as cleaned_file:
        cleaned_file.write('\n'.join(cleaned_times))

    return cleaned_times
        
      

print (cleaned_lines)
    
    
    
# -


