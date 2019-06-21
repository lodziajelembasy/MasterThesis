import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup

def get_addresses(n, base):
    addresses = []
    date_list = [base - datetime.timedelta(days=x) for x in range(0, n)]
    dates_cleaned = [str(x).replace('-','') for x in date_list]
    for date in dates_cleaned:
        ymd = date
        address = "http://mateusz.pl/czytania/" + ymd[:4]+ "/" + ymd + ".html"
        addresses.append(address)
    return addresses

def get_readings(address, day_name):
    page = requests.get(address)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        section = list(soup.children)
        section_content1 = section[2].find_all('p')
        if ((day_name == 'Sunday') or (len(section) in [32,34])):
            section_content2 = section[6]
            section_content3 = section[8]
            section_content4 = section[12]
        else:
            section_content2 = None
            section_content3 = section[4]
            section_content4 = section[8]
            
        pierwsze_czytanie = str(section_content1[6])
        drugie_czytanie = str(section_content2)
        tekst_przed_ewangelia = str(section_content3)
        psalm_ref = str(section_content1[7])
        psalm = ""
        i = 8
        while i < len(section_content1):
            psalm += str(section_content1[i])
            i += 1
        ewangelia = str(section_content4)
        document = [pierwsze_czytanie,psalm_ref,psalm, drugie_czytanie, tekst_przed_ewangelia, ewangelia]
        return document
    except:
        pass
        
def prepare_df():
    df_raw = pd.DataFrame(data=None, index=None, 
                  columns = ["Dzień tygodnia","Pierwsze czytanie", "Psalm_ref", "Psalm", "Drugie czytanie", 
                                                    "Werset przed Ewangelią", "Ewangelia"])
    return df_raw

def download_readings(n):
    df_raw = prepare_df()
    base = datetime.date.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(0, n)]
    dates_cleaned = [str(x).replace('-','') for x in date_list]
    dates_names = [x.strftime("%A") for x in date_list]
    addresses = get_addresses(n, base)

    for i in range(n):
            doc = get_readings(addresses[i], dates_names[i])
            input_row = [dates_names[i]]
            for each in doc:
                input_row.append(each)
            df_raw.loc[date_list[i]] = input_row
    return df_raw
