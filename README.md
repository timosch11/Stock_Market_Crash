**AvailableSymbols1:**

-> Python Programm which gets all the available Symbols which are offered by the financialmodelingprep API. It then inserts the 
data into a Table and creates a local JSON Copy. 

_**DailyHistData1:**

-> Python Programm seraches db for newest entry date, adds a day onto this date and takes the resulting data as a startdate for getting new
data for all following days. Formatting all the incoming data into the right format & load it into a db. With the for-loop it iterates through all existing stock symbols. --> Not in Use anymore.


**ETF_Country:**

-> R Programm which gets the available etf symbols from the db using a SQL-Statement and automatically itereates through that array to get all available ETF Country partitions.

**ETF_Sector:**

-> R Programm which gets all the available etf symbols from the db using a SQL-Statement and automatically iterates through that array to get all availabe ETF Sector partitions.

**Fundamental Data:**

-> Python Programm for getting all the information about the companys offered by the API. It creates a huge JSON Doc and appends all the incoming information. At the end of the process some formatting into valide JSON is done right before the data gets load into the DB.

**Improved_Daily_Hist_Data:**

-> Python Programm with same principle as the old one but some improvements were made.

**SamplyRun:**

-> Python Programm to try the execution of the Programm with the first n symbols. Gets fundamental data & daily stock prices.
1. Install requirements.txt
2. Change Path in Settings
3. Run

**Settings:**

-> Settings where you can activate either engine 1 (PostgreSQL DB) or engine 2 (SQL Server). SQL Server is default.
You can also choose the path where local docs are getting saved. 

**GetCurrency:**

--> For the conversion of the currencys in PostgreSQL.

