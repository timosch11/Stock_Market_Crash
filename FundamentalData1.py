import pandas as pd
import psycopg2
import os
import matplotlib
from sqlalchemy import create_engine
import requests
import json
import numpy as np
import Settings

#Json -> Combine Json to one File -> Load it into DB

# DataBaseConnection:
db_password = Settings.db_password
engine = Settings.engine

# path
csv_path = Settings.csv_path

symbols = []


def get_symbols_to_array(): #JSON-Documents with all Stocks the API offers
    df = pd.read_json("{}\Symbols.json".format(csv_path))
    # df =  df.to_csv()

    df = df.to_numpy() # df to 2d numpy Array
    # print(df)
    df = df[:, 0]   # Extrahieren der Symbols (US)
    return(df)

#symbols = get_symbols_to_array()   # Array with all US-Symbols

#print(symbols)

def get_fund_data_from_api(symbols): # Iterieren durch Array und für jedes Symbol die JSON zu den Fundamentalen Daten anfordern (ca. 4h dauer)

        for i in symbols:
            request = requests.get(
                "https://financialmodelingprep.com/api/v3/profile/{}?apikey=ab1eb63d17e1f21ebe847fe71162b752".format(i))

            with open(csv_path + r"\Fundamentals.json", 'a') as f:
                json.dump(request.json(), f)

            print("{} fundamental Data imported".format(i))

#get_fund_data_from_api(symbols)


def clean_json_to_csv():  # making the combination of multiple jsons a valid json
    # Delete all [ between json objects
    with open('{}/{}.json'.format(csv_path, "Fundamentals"), 'r') as infile, \
            open('{}/{}.json'.format(csv_path, "Fundamentals1"), 'w') as outfile:
        data = infile.read()
        data = data.replace("[", "")
        data = data.replace("]", "")
        data = data.replace("}", "},")

        outfile.write(data)

    with open('{}/{}.json'.format(csv_path, "Fundamentals1"), 'a') as the_file:
        the_file.write(']')

    with open('{}/{}.json'.format(csv_path, "Fundamentals1"), "r+") as f:
            a = f.read()
    with open('{}/{}.json'.format(csv_path, "Fundamentals1"), "w+") as f:
        f.write("[" + a)

    with open('{}/{}.json'.format(csv_path, "Fundamentals1"), 'r') as infile, \
            open('{}/{}.json'.format(csv_path, "Fundamentals2"), 'w') as outfile:
        data = infile.read()
        # data = data.replace("[[{]", "}]")
        data = data.replace("},]", "}]")
        outfile.write(data)



        #os.remove('{}/{}.json'.format(csv_path, "Fundamentals1"))
   
        #os.rename('{}/{}.json'.format(csv_path, "Fundamentals2"),
          #  '{}/{}.json'.format(csv_path, "Fundamentals1"))
#clean_json_to_csv()


# Create Table
def create_table():  # Take JSON -> to CSV -> to DB
    # Import CSV
    df = pd.read_json('{}/{}.json'.format(csv_path, "Fundamentals2"))
    df = df.to_csv()

    with open("{}.csv".format("fund_data"), "w") as text_file:
        text_file.write(df)
    df = pd.read_csv("{}.csv".format("fund_data"))


    # Formate the Db
    df = df[["symbol", "price","beta", "volAvg", "mktCap", "lastDiv", "range", "changes", "companyName", "currency","cik", "isin",
            "cusip", "exchange", "exchangeShortName", "industry", "website", "description", "ceo", "sector", "country",
            "fullTimeEmployees", "phone", "address", "city", "state", "zip", "dcfDiff", "dcf", "image", "ipoDate","defaultImage","isEtf",
           "isActivelyTrading"]]
    # df['ipoDate'] = pd.to_datetime(df['date'])   -> throws error dont know why
    df = df.fillna(0)
    df['updated'] = pd.to_datetime('now')

    # WriteIntoDB
    df.to_sql('FundamentalData1', engine, if_exists='replace', index=False)

  

    print("Fundamental Data Table created")

#create_table()
