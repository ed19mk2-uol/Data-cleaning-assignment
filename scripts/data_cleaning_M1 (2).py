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
                formatted_time = dt.strftime("%d-%m-%Y %H:%M:%S")#converts it in to the format we need
                print(f"Original: {timestamp} -> Formatted: {formatted_time}")#fancy way of printing old and new

                cleaned_file.write(formatted_time + '\n')#writes the formatted time with a new line
            except ValueError:
                print(f"Skipping invalid timestamp: {timestamp}")#this skips any invalid lines
                continue#continues the loop



url="https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2023-01-01&endtime=2023-01-02"


data_lines = import_data(url)#input

if data_lines:
    clean_data(data_lines)#output

# +

    

    
    
    
# -


