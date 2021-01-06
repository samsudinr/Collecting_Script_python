import gspread
import pandas as pd
import lib_gspread as lib

cred = lib.cred_emcanalyticsteam
credentials = lib.authorize_credentials(cred)
gc = gspread.authorize(credentials)
id_source = gc.open_by_key("id-speadsheet")

# create dataframe
DF = pd.DataFrame({'Day': [31, 30, 31, 30], 'Month': ['Jan', 'Apr', 'Mar', 'June']})

try:
    lib.pandas_to_sheets(DF, id_source.worksheet("results"))
    print ("success import dataframe to spreadsheet")
except Exception as e:
    print(e)
    error = "Error import data to spreadsheet"
    print (error)
