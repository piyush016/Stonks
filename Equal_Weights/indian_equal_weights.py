from typing import final
import numpy as np #Faster calculation as this package is written in C/C++
import pandas as pd #Easier to work with tabular data
import requests #For http requests
import xlsxwriter #For well formatted excel document
import math #For operations

# ---------------------------------------------------------------------------- #
#                          Reading Nifty 50 stock name                         #
# ---------------------------------------------------------------------------- #
# stocks = pd.read_csv("./Equal_Weights/nifty50list.csv")
stocks = pd.read_csv("./nifty50list.csv")


# ----------------------------- Creating columns ----------------------------- #
my_columns = ["Ticker", "Stock Price", "Total Traded Volume", "Number of Shares to Buy"]
final_dataframe = pd.DataFrame(columns = my_columns)

# ---------------------------------------------------------------------------- #
#     Traversing through each stock to get the last-price and traded-volume    #
# ---------------------------------------------------------------------------- #
for stock in stocks["Ticker"]:
    # print(stock)
    api_url = f"http://localhost:3000/nse/get_quote_info?companyName={stock}" #Getting stock details
    data = requests.get(api_url).json()

    lastPrice = float(data["data"][0]["lastPrice"].replace(',', ''))
    
    final_dataframe = final_dataframe.append(
        pd.Series(
            [
                data["data"][0]["symbol"],
                lastPrice,
                data["data"][0]["totalTradedVolume"],
                "N/A"
            ],
            index=my_columns),
            ignore_index = True
    )
#print(final_dataframe)

# ---------------------------------------------------------------------------- #
#                          For Number of stocks to buy                         #
# ---------------------------------------------------------------------------- #
portfolioSize = input("Enter the value of your portfolio: ")
# ------------------ Checking if the input is number or not ------------------ #
try: 
    val = float(portfolioSize) 
except ValueError:
    print("That's not a number!!")
    portfolioSize = input("Enter a value of your portfolio: ")
    val = float(portfolioSize)

print(f"Your entered PORTFOLIO SIZE: Rs {val}")

position_size = val / len(final_dataframe.index) #Diving the portfolio in equal weights
for i in range (0, len(final_dataframe.index)):
    final_dataframe.loc[i, "Number of Shares to Buy"] = math.floor(position_size/final_dataframe.loc[i, "Stock Price"])

#print(final_dataframe)


# ---------------------------------------------------------------------------- #
#              Writing the dataframe in the excel using xlsxwriter             #
# ---------------------------------------------------------------------------- #
writer = pd.ExcelWriter("Recommended Trades.xlsx", engine="xlsxwriter") #Initializing the file
final_dataframe.to_excel(writer, "Recommended Trades", index=False)
color1 = "#EC4176" #brightPink
color2 = "#A13670" #darkPink
color3 = "#FFA45E" #yellow
color4 = "#262254" #violet
color5 = "#607D3B" #green
color6 = "#FFFFFF" #white 

string_format = writer.book.add_format(
    {
        "font_color": color1,
        "bg_color": color3,
        "border": 1
    }
)

dollar_format = writer.book.add_format(
    {
        "num_format": "Rs0.00",
        "font_color": color2,
        "bg_color": color4,
        "border": 1
    }
)


integer_format = writer.book.add_format(
    {
        "num_format": "0",
        "font_color": color6,
        "bg_color": color5,
        "border": 3
    }
)



column_formats = {
    "A": ["Ticker", string_format],
    "B": ["Stock Price", dollar_format],
    "C": ["Total Traded Volume", string_format],
    "D": ["Number of Shares to Buy", integer_format],
}

for column in column_formats.keys():
    writer.sheets["Recommended Trades"].set_column(f"{column}:{column}", 25, column_formats[column][1])
    writer.sheets["Recommended Trades"].write(f"{column}1", column_formats[column][0], column_formats[column][1])
writer.save()
print("CSV file saved!!!")