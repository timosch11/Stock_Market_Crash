# Title     : TODO
# Objective : TODO
# Created by: timos
# Created on: 30.04.2021

install.packages(c("httr", "jsonlite"))
install.packages("rjson")
install.packages('RPostgreSQL')
install.packages('devtools')
install.packages('remotes')
install.packages('RPostgres')

library(httr)
library(jsonlite)
library(rjson)
library(DBI)

api_key =  "?apikey=ab1eb63d17e1f21ebe847fe71162b752"
api_url_for_etfs = "https://financialmodelingprep.com/api/v3/symbol/available-etfs?apikey=ab1eb63d17e1f21ebe847fe71162b752"
api_url_for_sectorspt1 = "https://financialmodelingprep.com/api/v3/etf-sector-weightings/"


req = httr::GET("https://financialmodelingprep.com/api/v3/symbol/available-etfs?apikey=ab1eb63d17e1f21ebe847fe71162b752")
req$status_code
char <- rawToChar(req$content)
df <- jsonlite::fromJSON(char)
df =

symbols = df$symbol
symbols
symbols[333]

df1 <- data.frame(df1)




options(max.print=1000000)

df1 <- NULL
df1 <- data.frame(df1,row.names = "sector","weightPercentage","ETF")



      for(symbols in symbols){
       tryCatch({

       url = paste(api_url_for_sectorspt1,symbols,api_key,sep = "")
       req1 = httr::GET(url)
       char1 <- rawToChar(req1$content)

       df2 <- jsonlite::fromJSON(char1)
       df2$ETF = symbols

       df1 <- rbind(df1, df2)
      },error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
                         }

 symbols[333]

 #
 for(symbols in symbols){ print(symbols)}

 url = paste(api_url_for_sectorspt1,symbols[3],api_key,sep = "")
 url
 req1 = httr::GET(url)
 req1
 char1 <- rawToChar(req1$content)
 char1
 df2 <- jsonlite::fromJSON(char1)
 df2
 df2$ETF = symbols[3]
 df1 = df2
 df1 <- rbind(df1, df2)
 df1
#


db <- 'StockData'

host_db <- 'localhost' #i.e. # i.e. 'ec2-54-83-201-96.compute-1.amazonaws.com'

db_port <- '5432'  # or any other port specified by the DBA

db_user <- 'postgres'

db_password <- 'wkb6'

con <- dbConnect(RPostgres::Postgres(), dbname = db, host=host_db, port=db_port, user=db_user, password=db_password)

dbWriteTable(con, name='ETFSectors',value=df1, overwrite =TRUE)

df1


worked = dbGetQuery(con,'Select distinct "ETF" from public."ETFSectors"')


worked = worked$ETF
worked[2]



