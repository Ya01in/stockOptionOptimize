# yaolin
# first spider 
# getting the company and their id using requests
from cgitb import text
import pandas as pd
import requests 

header = {
    "User-Agent":
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
}

html_raw = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2", headers = header)

if html_raw.status_code != 200:
    print(html_raw.status_code)
    exit(0)

##text is for unicode data, content is for binary
text = pd.read_html(html_raw.text)

## get dataframe
target = text[0]

target.columns = target.iloc[0,:]
target = target.iloc[1:, :].copy()

## split value using lamda 
target['代號'] = target['有價證券代號及名稱'].apply(
    lambda target: target.split()[0]).copy()
target['股票名稱'] = target['有價證券代號及名稱'].apply(
    lambda target: target.split()[-1]).copy()

target['上市日'] = pd.to_datetime(target['上市日'], errors='coerce')
target = target.dropna(subset=['上市日'])

target.drop(["有價證券代號及名稱", "國際證券辨識號碼(ISIN Code)"
, "CFICode", "備註"], axis=1)
target = target[['代號', '股票名稱', '上市日', '市場別', '產業別']]
target = target.dropna(subset=['產業別'])

# print(target)
target.to_excel('./todayStockList.xlsx')