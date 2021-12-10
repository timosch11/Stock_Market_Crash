import pandas as pd
import psycopg2
import os
import matplotlib
from sqlalchemy import create_engine
import requests
import json
import numpy as np
import AvailableSymbols1,FundamentalData1, Improved_Daily_Hist_Data, Settings

# A Run with the first 100 Stock Symbols to show functionality

NumberOfStocks = 100
highestDate = '2020-01-01'
AvailableSymbols1.get_data()
symbolsSliced = FundamentalData1.get_symbols_to_array()[:NumberOfStocks]

FundamentalData1.get_fund_data_from_api(symbolsSliced)
FundamentalData1.clean_json_to_csv()
FundamentalData1.create_table()
Improved_Daily_Hist_Data.get_api_and_write_into_db(symbolsSliced,highestDate)



