import pandas as pd
import requests

import json
import Settings

from sqlalchemy import create_engine




#Get All the available Stock Symbols and the ability to get it into DB
db_password = Settings.db_password
engine = Settings.engine
csv_path = Settings.csv_path

def get_data():
    request = requests.get(
        "https://financialmodelingprep.com/api/v3/stock/list?apikey=ab1eb63d17e1f21ebe847fe71162b752")  #API Call

    with open("{}\Symbols.json".format(csv_path), 'w') as f:
        json.dump(request.json(), f)  #Speicher hier


# get_data()





def create_symbols_table():
    df = pd.read_json("{}\Symbols.json".format(csv_path))
    df.to_csv()
    df = df[['symbol', 'name', 'price', 'exchange']]
    df = df.fillna(0)
    df['updated'] = pd.to_datetime('now')
    df.to_sql('Symbols_NYSE', engine, if_exists='replace', index=True)


