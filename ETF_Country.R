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
api_url_for_sectorspt1 = "https://financialmodelingprep.com/api/v3/etf-country-weightings/"



db <- 'StockData'

host_db <- 'localhost'

db_port <- '5432'  # or any other port specified by the DBA

db_user <- 'postgres'

db_password <- 'wkb6'

con <- dbConnect(RPostgres::Postgres(),
                 dbname = db,
                 host=host_db,
                 port=db_port,
                 user=db_user,
                 password=db_password)




GetCountrys <- function(){

  worked = dbGetQuery(con,'SELECT distinct "symbol" FROM public."Fundamental Data" as fd
inner join public."dailyprices"  as dp on dp.stock = fd.symbol
where "isEtf" = TRUE')
  worked = worked$symbol

  worked

  url = paste(api_url_for_sectorspt1,worked[4],api_key,sep = "")
  req1 = httr::GET(url)
  char1 <- rawToChar(req1$content)
  df2 <- jsonlite::fromJSON(char1)
  df2
  df2$ETF = symbols
  df2
  df1 = df2
  for(symbols in worked){
    tryCatch({

      url = paste(api_url_for_sectorspt1,symbols,api_key,sep = "")
      req1 = httr::GET(url)
      char1 <- rawToChar(req1$content)

      df2 <- jsonlite::fromJSON(char1)
      df2$ETF = symbols

      df1 <- rbind(df1, df2)
      Sys.sleep(0,01)
    },error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
  }

  dbWriteTable(con, name='ETF_DataCountry2',value=df1, overwrite =TRUE)

  return (df1)
}

GetCountrys()
