from selenium import webdriver
import time
import gspread
from datetime import date
import pandas as pd
import lib_gspread as lib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cred = lib.cred_emcanalyticsteam
credentials = lib.authorize_credentials(cred)
gc = gspread.authorize(credentials)

today   = date.today()
date_crawl = today.strftime("%Y-%m-%d")

CHROMEPATH = 'path-of-your-chrome/chromedriver.exe'

def get_info(links):
    try:
        driver = webdriver.Chrome(CHROMEPATH)
        driver.get(links)
        time.sleep(5)
        cs_selector = "#count > yt-view-count-renderer > span.view-count.style-scope.yt-view-count-renderer"
        e = driver.find_element(By.CSS_SELECTOR,cs_selector)
        time.sleep(3)
        res = e.text.split(" ")[0]
        res = int(res.replace(",", ""))
        print(res)
        return res
    except :
        print "error"
        return 0

id_source = gc.open_by_key("id-file-spreadsheet")
time.sleep(3)
id_results = gc.open_by_key("id-file-spreadsheet")
time.sleep(3)

sheet_name = id_source.worksheet('config')
rows = sheet_name.get_all_values()
sharp_Q3 = pd.DataFrame.from_records(rows)
print (sharp_Q3)
headers = sharp_Q3.iloc[0]
sharp_Q3 = sharp_Q3[1:]
sharp_Q3.columns = headers

sheet_result = id_results.worksheet('results')
rows_ = sheet_result.get_all_values()
old_data = pd.DataFrame.from_records(rows_)
headers_ = old_data.iloc[0]
old_data = old_data[1:]
old_data.columns = headers_

sharp_Q3 = sharp_Q3[sharp_Q3['Platform']=="youtube"].reset_index(drop=True)
new_data = sharp_Q3.copy()
new_data['Date'] = date_crawl
new_data['Views Video 1'] = new_data['Video URL 1'].apply(lambda x: "" if x == "" else get_info(x))
new_data['Views Video 2'] = new_data['Video URL 2'].apply(lambda x: "" if x == "" else get_info(x))
new_data = new_data[['Platform', 'Date', 'Client', 'Channel', 'Product', 'Video URL 1', 'Video URL 2', 'Views Video 1', 'Views Video 2']]
print (new_data)

new_data.loc[new_data['Views Video 1'] == 0 ] = get_info(new_data['Video URL 1'])
new_data.loc[new_data['Views Video 2'] == 0 ] = get_info(new_data['Video URL 2'])

results = old_data.append(new_data)

try:
    lib.pandas_to_sheets(results, id_results.worksheet("results"))
    print ("success import dataframe to spreadsheet")
except Exception as e:
    print(e)
    error = "Error admonitoring prediction"
    print (error)


