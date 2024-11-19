import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import re

# 目標URL
symbol = "DELL"
url = f'https://www.lietabackend.com/gex/{symbol}?dte=7'

# 發送GET請求
response = requests.get(url)

# 確認請求是否成功
if response.status_code == 200:
    html_doc = response.text
    
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    # 抓取所有的 <script> 標籤
    res = soup.find_all('script')
    
    # 假設你要的目標是第3個<script>標籤
    target = res[2]
    
    # 使用正則表達式定位所需的JSON片段
    start_piv = re.search('alignmentgroup', target.text)
    start_idx = start_piv.start() - 3

    end_piv = re.search(r'bar"\},\{"line"', target.text)
    end_idx = end_piv.start() + 5

    # 抽取JSON字串並解析
    json_str = target.text[start_idx:end_idx] + ']'
    data = json.loads(json_str)

    # 處理資料，將數值轉換為百萬（M），並格式化保留兩位小數
    record = {}
    for i, d in enumerate(data):
        for j, price in enumerate(d['y']):
            value_in_million = d['x'][j]
            #value_in_million = float(f"{value_in_million:.2f}")  # 保留兩位小數並轉為浮點數
            if price in record:
                record[price] += value_in_million
            else:
                record[price] = value_in_million

    # 將結果格式化輸出，保證每個數字保留兩位小數
    formatted_record = {k: float(f"{v:.2f}") for k, v in record.items()}
    
    # 輸出結果
    pprint(formatted_record)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
def analyze_gamma(formatted_record):
    positive_gamma = {price: int(value) for price, value in formatted_record.items() if value > 0}
    negative_gamma = {price: int(value) for price, value in formatted_record.items() if value < 0}

    # Calculate sums
    positive_sum = sum(positive_gamma.values())
    negative_sum = abs(sum(negative_gamma.values()))  # Take absolute value for comparison

    # Calculate percentage ratio
    ratio = round((positive_sum / negative_sum), 2) if negative_sum != 0 else "All Positive"

    import numpy as np
    positive_exceed_price, positive_exceed_ratio = 0, 0
    negative_lower_price, negative_lower_ratio = 0, 0

    if positive_sum > 0:
        positive_values = list(positive_gamma.values())
        positive_mean = np.mean(positive_values)
        positive_std = np.std(positive_values)
        positive_outliers = {price: value for price, value in positive_gamma.items()
                             if value > positive_mean + 3 * positive_std}
        if len(positive_outliers) == 1:
            # Take the only (price, value) from the outliers
            positive_exceed_price = list(positive_outliers.keys())[0]
            positive_exceed_ratio = round(((positive_outliers[positive_exceed_price] - positive_mean) / positive_mean), 2)

    if negative_sum > 0:
        negative_values = list(negative_gamma.values())
        negative_mean = np.mean(negative_values)
        negative_std = np.std(negative_values)
        negative_outliers = {price: value for price, value in negative_gamma.items()
                             if value < negative_mean - 3 * negative_std}
        if len(negative_outliers) == 1:
            # Take the only (price, value) from the outliers
            negative_lower_price = list(negative_outliers.keys())[0]
            negative_lower_ratio = round(((negative_mean - negative_outliers[negative_lower_price]) / abs(negative_mean)), 2)

    return {
        "Positive Sum": positive_sum,
        "Negative Sum": negative_sum,
        "Ratio (P/N)": ratio,
        "Positive Exceed 3 sigma Price": positive_exceed_price,
        "Positive Exceed 3 sigma/Mean Ratio": positive_exceed_ratio,
        "Negative Lower 3 sigma Price": negative_lower_price,
        "Negative Lower 3 sigma /Mean Ratio": negative_lower_ratio
    }

pprint(analyze_gamma(formatted_record))
