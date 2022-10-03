import pandas as pd

print("Welcome to stock market analysis.")
print("What do you wanna know? ")
ans = input(" 1.Rights\n 2.Bonus\n 3.Splits\n 4.Dividend\n")

print("Collecting data for you....")

if ans == "1":
    table = pd.read_html("https://www.moneycontrol.com/stocks/marketinfo/rights/index.php")
    #print(table[1])
    table[1].to_csv("stock_rights.csv")

elif ans == "2":
    table = pd.read_html("https://www.moneycontrol.com/stocks/marketinfo/bonus/index.php?sel_year=2022")
    #print(table[1])
    table[1].to_csv("stock_bonus.csv")

elif ans == "3":
    table = pd.read_html("https://www.moneycontrol.com/stocks/marketinfo/splits/index.php")
    #print(table[1])
    table[1].to_csv("stock_split.csv")

elif ans == "4":
    table = pd.read_html("https://www.moneycontrol.com/stocks/marketinfo/dividends_declared/index.php?sel_year=2022")
    #print(table[1])
    table[1].to_csv("stock_dividend.csv")

print("Market analysis finished!!!")