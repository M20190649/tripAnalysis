

# import usaddress
# usaddress.parse('1320 WI-190, Shorewood, WI 53211, USA')

from requests import get
from pprint import pprint
from json import dump
from csv import QUOTE_ALL, DictWriter
import pandas as pd
import time




with open('../Google_API_Jin.txt' ) as file:
    API_KEY  = file.read()
# API_KEY = 'AIzaSyAoPQQo1UX3BRKhUAYFzzW294wVFnFfs7Y'
def address_resolver(json):
    final = {}
    if json['results']:
        data = json['results'][0]
        for item in data['address_components']:
            for category in item['types']:
                data[category] = {}
                data[category] = item['long_name']
        final['street'] = data.get("route", None)
        final['state'] = data.get("administrative_area_level_1", None)
        final['city'] = data.get("locality", None)
        final['county'] = data.get("administrative_area_level_2", None)
        final['country'] = data.get("country", None)
        final['postal_code'] = data.get("postal_code", None)
        final['neighborhood'] = data.get("neighborhood",None)
        final['sublocality'] = data.get("sublocality", None)
        final['housenumber'] = data.get("housenumber", None)
        final['postal_town'] = data.get("postal_town", None)
        final['subpremise'] = data.get("subpremise", None)
        final['latitude'] = data.get("geometry", {}).get("location", {}).get("lat", None)
        final['longitude'] = data.get("geometry", {}).get("location", {}).get("lng", None)
        final['location_type'] = data.get("geometry", {}).get("location_type", None)
        final['postal_code_suffix'] = data.get("postal_code_suffix", None)
        final['street_number'] = data.get('street_number', None)
    return final


def get_address_details(address, 
                        dictAB= {"A": "UW-Milwaukee", "B": "UWM"},
                        Choice="A"):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?components=&language=&region=&bounds=&key='+ API_KEY
    AdditionAddress = address + dictAB[Choice]
    url = url + '&address='+ AdditionAddress.replace(" ","+")
    response = get(url)
    data  = address_resolver(response.json())
    data['address'] = address 
    return data

get_address_details("sandburg ")


if __name__ == '__main__':
    """
    Provide the address via csv or paste it here 
    """
    start = time.time()
    print("hello")
    dictAB = {"A": "UW-Milwaukee", "B": "UWM"}
    Choice = "A"

    Rela_ad = 'inprocess_results/'
    path = Rela_ad + 'outliersPick Up Location.csv'

    outfile01 = Rela_ad + "Request_data_test" + "PK"  +".csv"

    df = pd.read_csv(path,delimiter='\n', header= None)
    address_to_search = list(df[0])
    # address_to_search = list(csv.DictReader("outliers.csv"))
    # address_to_search = ['Starbucks - Downer']
    data = []
    for i in address_to_search:
        data.append(get_address_details(i,dictAB,Choice ))
        
    with open(outfile01,'w') as csvfile:
        csvwriter = DictWriter(csvfile, fieldnames=data[0].keys(), quoting=QUOTE_ALL)
        csvwriter.writeheader()
        csvwriter.writerows(data)

    
    end = time.time()
    print(str(int((end - start)/60)) + ' min' )


# json = response.json()