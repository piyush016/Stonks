import numpy as np #Faster calculation as this package is written in C/C++
import pandas as pd #Easier to work with tabular data
import requests #For http requests
import xlsxwriter #For well formatted excel document
import math #For operations
from keys import IEX_CLOUD_API_TOKEN

# Creating Batch for faster API CALLS
def chunks(lst, n):
    for i in range (0, len(lst), n):
        yield lst[i:i + n]


#Importing CSV file
stocks = pd.read_csv("./Equal_Weights/sp_500_stocks.csv")
stocks = stocks[~stocks['Ticker'].isin(['DISCA', 'HFC','VIAC','WLTW'])] #Delisted Stocks
# print(stocks)

# symbol = "AAPL"
# api_url = f"https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}" #base URL
# #API URL + symbol which is the company + key/token
# #print(api_url) ##To check the API CALL

# data = requests.get(api_url).json() #Converting the data into json
# # print(data)  ##To check what kind of data are we getting
# # print(data.status_code) ##To check the status code

# price = data['latestPrice']
# market_cap = data['marketCap']
# # print(price)
# # print(market_cap)

my_columns = ["Ticker", "Stock Price", "Market capitalization", "Number of Shares to Buy"] #Columns
final_dataframe = pd.DataFrame(columns = my_columns)
# # print(final_dataframe)  ##To see how dataframe looks like

# final_dataframe.append(
#     pd.Series(
#         [
#             symbol,
#             price,
#             market_cap,
#             'N/A'
#         ],
#     index = my_columns,
#     ),
#     ignore_index=True #Just Add this in the end
# )

######### Above process for single Stock ###########


########## For Multiple Stocks ############
# final_dataframe = pd.DataFrame(columns= my_columns)
# for stock in stocks['Ticker'][:3]: #Looping only for 3 stocks for now because the process is slow
#     # print(stock)
#     api_url = f"https://sandbox.iexapis.com/stable/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}"
#     data = requests.get(api_url).json() 
#     final_dataframe = final_dataframe.append(
#         pd.Series(
#             [
#                 stock,
#                 data['latestPrice'],
#                 data['marketCap'],
#                 'N/A'
#             ],
#             index=my_columns),
#             ignore_index=True
#     )
# print(final_dataframe)



####### Creating batches of 100 for faster API Call ##########
symbol_groups = list(chunks(stocks['Ticker'], 100)) #Chucnk function call which is defined above
symbol_strings = []
# print(symbol_groups)
for i in range (0, len(symbol_groups)): #Grouping the list of 100
    symbol_strings.append(','.join(symbol_groups[i]))

final_dataframe = pd.DataFrame(columns=my_columns)
for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
    print(batch_api_call_url)
    data = requests.get(batch_api_call_url).json() #Converting data to JSON
    # print(data.status_code) ##Do this without putting JSON at the end
    for symbol in symbol_string.split(","):
    #    print(symbol)
        final_dataframe = final_dataframe.append(
        pd.Series(
            [
                symbol,
                data[symbol]['quote']['latestPrice'],
                data[symbol]['quote']['marketCap'],
                'N/A'
            ], index = my_columns
        ), ignore_index=True
        )
    
# print(final_dataframe)

####For no. of shares to buy####
portfolio_size = input("Enter the value of your portfolio: ")
try: #Checking of the input is number
    val = float(portfolio_size)
except ValueError:
    print("That's not a number!!")
    portfolio_size = input("Enter the value of your portfolio: ")
    val = float(portfolio_size)

print(val) 

position_size = val / len(final_dataframe.index)
for i in range(0, len(final_dataframe.index)):
    final_dataframe.loc[i, "Number of Shares to Buy"] = math.floor(position_size/final_dataframe.loc[i, "Stock Price"])
print(final_dataframe)


#### Writing the dataframe in excel using xlsxwriter ####

writer = pd.ExcelWriter("Recommended Trades.xlsx", engine="xlsxwriter") #Initializing the file
final_dataframe.to_excel(writer, "Recommended Trades", index=False)

background_color = "#0a0a23"
font_color = "#ffffff"

string_format = writer.book.add_format(
    {
        "font_color": font_color,
        "bg_color": background_color,
        "border": 1
    }
)

dollar_format = writer.book.add_format(
    {
        "num_format": "$0.00",
        "font_color": font_color,
        "bg_color": background_color,
        "border": 1
    }
)


integer_format = writer.book.add_format(
    {
        "num_format": "0",
        "font_color": font_color,
        "bg_color": background_color,
        "border": 1
    }
)



column_formats = {
    "A": ["Ticker", string_format],
    "B": ["Stock Price", dollar_format],
    "C": ["Market Capitalization", dollar_format],
    "D": ["Number of Shares to Buy", integer_format],
}

for column in column_formats.keys():
    writer.sheets["Recommended Trades"].set_column(f"{column}:{column}", 18, column_formats[column][1])
    writer.sheets["Recommended Trades"].write(f"{column}1", column_formats[column][0], column_formats[column][1])
writer.save()