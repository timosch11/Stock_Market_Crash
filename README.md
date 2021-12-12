**AvailableSymbols1:**

-> Python Programm which receives all the available symbols that are offered by the financialmodelingprep API. It then inserts the 
data into a table and creates a local JSON copy. 

_**DailyHistData1:**

-> Python Programm searches database for newest entry date, adds a day onto this date and takes the resulting data as a startdate for getting new
data for all following days. Formatting all the incoming data into the right format & load it into a database. With the for-loop it iterates through all existing stock symbols. --> Not in use anymore.


**ETF_Country:**

-> R Programm which gets the available etf symbols from the database using a SQL-Statement and automatically itereates through that array to get all available ETF country partitions.

**ETF_Sector:**

-> R Programm which gets all the available etf symbols from the database using a SQL-Statement and automatically iterates through that array to get all availabe ETF sector partitions.

**Fundamental Data:**

-> Python Programm for getting all the information about the companies offered by the API. It creates a huge JSON doc and appends all the incoming information. At the end of the process, some formatting into valid JSON is done, right before the data gets uploaded into the database.

**Improved_Daily_Hist_Data:**

-> Python Programm with the same principle as the old one but some improvements were made.

**SamplyRun:**

-> Python Programm to try the execution of the programm with the first n symbols. Gets fundamental data & daily stock prices.
1. Install requirements.txt
2. Change path in settings
3. Run

**Settings:**

-> Settings, where you can activate either engine 1 (PostgreSQL DB) or engine 2 (SQL Server). SQL Server is default.
You can also choose the path, where local docs are getting saved. 

**GetCurrency:**

--> For the conversion of the currencies in PostgreSQL.

