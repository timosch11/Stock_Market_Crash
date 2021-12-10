import pandas as pd
import psycopg2
import os
import matplotlib
from sqlalchemy import create_engine
import requests
import json
import re
import datetime
import io
import Settings
#Get Data as JSON -> Formate JSON -> to CSV -> to Insert Statement

# DataBaseConnection:
db_password = Settings.db_password #Passwort for PGDB
engine = Settings.engine #ConnectionString
last_date = engine.execute("""Select max(date) from public.dailyprices""")

# path
csv_path = r'C:\Users\timos\Documents\HTML\python-eodhistoricaldata\CSV_try'
json_path = r"C:\Users\timos\Documents\HTML\python-eodhistoricaldata\JSON_try"
failcount = 0

def get_highest_date():
    for row in last_date:
        result = row
    datetim = datetime.datetime(int(row[0][0:4]), int(row[0][5:7]), int(row[0][8:10]))
    datetim += datetime.timedelta(days=1)
    return str(datetim)[0:10]
print(get_highest_date())


def get_symbols_to_array():  # JSON-Documents with all Stocks the API offers
    df = pd.read_json(r"C:\Users\timos\Documents\HTML\python-eodhistoricaldata\CSV_try\Symbols.json")  #Auslesen der JSON
    symbols = []
    df = df.to_numpy()  # df to 2d numpy Array
    df = df[:, 0]  # Extrahieren der Symbols (US)
    return (df)  #Returns List with all available Stock Symbols

def get_prices(StockSymbol):  #Gets hist. Data and write it as JSON
    request = requests.get(
        "https://financialmodelingprep.com/api/v3/historical-price-full/{}?from={}&apikey=ab1eb63d17e1f21ebe847fe71162b752".format(
            StockSymbol, get_highest_date()))  #APICall

    with open(r'C:\Users\timos\Documents\HTML\python-eodhistoricaldata\JSON_try\{}.json'.format(StockSymbol), 'w') as f:
        json.dump(request.json(), f)  #Write into JSON-File


#StockSymbol = get_symbols_to_array()


def formatting(StockSymbol): # Getting the JSON-File ready to Format into CSV-File
 try:  #IF API Call turns back an unusal  answer the program shouldn't Crash (Happens if the API returned nothing)
    df = pd.read_json(r'C:\Users\timos\Documents\HTML\python-eodhistoricaldata\JSON_try\{}.json'.format(StockSymbol))
    df = df.to_csv()   #to_csv don't work as thought therefore we have to resolve the hist. Data Array in JSON-File

    abhier = df.index("{")  # Getting Index for everything before {
    df = df[abhier:]  #Remove everything before
    df = "[" + df + "]"   #Insert [ at the Start & ] at the end
    df = re.sub("\d{1,3},\w*.{0,1}\w{1,2},", "}", str(df)) # Regex to format File

    df = re.sub('}"{', ',"{', df)
    df = re.sub('"\s+,"', ",", df)
    df = re.sub("'", '"', df)
    df = re.sub('}"\s+]', '}]', df)

    data = io.StringIO(df)
    df = pd.read_json(data)   #Rewrite File
    return df
 except Exception as e:
        print("{} failed to import".format(StockSymbol) + str(e))
        failcount+1

def create_table(StockSymbol,df):  #Create new Table into PGDB

    #df = pd.read_json(r"C:\Users\timos\Documents\HTML\python-eodhistoricaldata\Csv\{}.json".format(StockSymbol),
    #                  orient='records') # Read Formatted-JSON
    df = df.to_csv()  #Turn to CSV
    df = "index" + df   #Add Index Column
    data = io.StringIO(df)
    df = pd.read_csv(data)  #Read it out

    # Formate the Db

    df = df[["index", "date", "open", "high", "low", "close", "adjClose", "volume", "unadjustedVolume", "change",
             "changePercent", "vwap", "label", "changeOverTime"]]  #Define the Headers
    # df['ipoDate'] = pd.to_datetime(df['date'])   -> throws error dont know why
    df = df.fillna(0)  #FillEmptyColumns
    df['stock'] = StockSymbol   #Add Stock Symbol to identify
    df['updated'] = pd.to_datetime('now')   #Add timestamp

    # WriteIntoDB
    df.to_sql('dailyprices2', engine, if_exists='replace', index=False)  #Define Table Name and Execute

    print("PriceData Table created")
    print("{} imported".format(StockSymbol))


def import_csv_into_table(StockSymbol,df):
    try:   #If an Error Occures don't let the Programm Crash

        df = df.to_csv()  # Turn to CSV
        df = "index" + df  # Add Index Column
        data = io.StringIO(df)
        df = pd.read_csv(data)
        # Clean
        df = df.fillna(0)

        df = df[["index", "date", "open", "high", "low", "close", "adjClose", "volume", "unadjustedVolume", "change",
                 "changePercent", "vwap", "label", "changeOverTime"]]  #Define Headers

        df['stock'] = StockSymbol  # Add Symbol
        df['updated'] = pd.to_datetime('now')  #Add Timestamp
        #Create INSERT-Statement with pandas iterrow:
        insert_statement = """INSERT INTO DailyPrices
     VALUES """

        values = ",".join(["""('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'
                     )""".format(

            index,
            row.date,
            row.open,
            row.high,
            row.low,
            row.close,
            row.adjClose,
            row.volume,
            row.unadjustedVolume,
            row.change,
            row.changePercent,
            row.vwap,
            row.label,
            row.changeOverTime,
            StockSymbol,
            pd.to_datetime('now')

        ) for index, row in df.iterrows()])


        query = insert_statement + values   #Clue it together
        engine.execute(query)  #Execute SQL onto Engine
        print("{} imported".format(StockSymbol))   #Print out
    except Exception as e:    #Errorhandling
        print("{} failed to import".format(StockSymbol) + str(e))
        failcount+1

def get_api_and_write_into_db(StockSymbol):     #Main
    #Do the Create Table Process 1 time:
    get_prices(StockSymbol[0])
    formatting(StockSymbol[0])
    create_table(StockSymbol[0])
    #Do the Insert Process the rest of the time
    for i in range(1, len(StockSymbol)):
        get_prices(StockSymbol[i])
        formatting(StockSymbol[i])
        import_csv_into_table(StockSymbol[i])

    print("Updated successfully! But {} errors occured ".format(failcount))


#get_api_and_write_into_db(StockSymbol)
