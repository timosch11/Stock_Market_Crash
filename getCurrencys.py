from forex_python.converter import CurrencyRates
from datetime import datetime
import pandas as pd
from datetime import date
from dateutil.rrule import rrule, DAILY
from sqlalchemy import create_engine
import Settings


daterange = pd.date_range(start='1/1/2020', end='5/1/2021')
c = CurrencyRates()
db_password = Settings.db_password
engine = Settings.engine


def getCurrency():
    rates = c.get_rates("EUR", pd.to_datetime('31/12/2019'))
    df = pd.DataFrame.from_dict(rates, orient='index')
    # df2 = df2.transpose()
    df.reset_index(level=0, inplace=True)
    df["Date"] = pd.to_datetime('31/12/2019')
    df.columns = ["Currency", "Value", "Date"]
    new_rows = {"Currency":"EUR","Value":1,"Date":pd.to_datetime('31/12/2019')}
    df = df.append(new_rows, ignore_index=True)
    for date in daterange:
        rates = c.get_rates("EUR", date)
        df2 = pd.DataFrame.from_dict(rates, orient='index')
        # df2 = df2.transpose()
        df2.reset_index(level=0, inplace=True)
        df2["Date"] = date
        df2.columns = ["Currency", "Value", "Date"]
        new_rows = {"Currency": "EUR", "Value": 1, "Date": date}
        df2 = df2.append(new_rows,ignore_index=True)
        df = pd.concat([df2, df])

        print(df)

    return df

df = getCurrency()
#df.to_sql('CurrencyRates', engine, if_exists='replace', index=False)
