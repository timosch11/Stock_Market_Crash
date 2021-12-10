from sqlalchemy import create_engine
import pyodbc
import datetime as dt
db_password = "wkb6"
zieldbmssql = "Infosys"
#engine = create_engine('postgresql://postgres:{}@localhost:5432/StockData'.format(db_password))
engine = create_engine('mssql+pyodbc://wkb6:{}@itnt0005/{}?driver=SQL+Server'.format(db_password,zieldbmssql))
csv_path = r' '  #Insert Path here for example 'C:\Users\timo\Untitled Folder'
json_path = r' '  #Insert Path here





