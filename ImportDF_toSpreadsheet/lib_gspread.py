import httplib2
import pandas as pd
import gspread
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

cred_emcanalyticsteam = {
    'pathClientSecret': 'cred/client_secret_yourEmail.json',
    'pathTokenDrive': 'cred/token_drive_yourEmail.pickle'
}

# Start the OAuth flow to retrieve credentials
def authorize_credentials(dict):
    CLIENT_SECRET = dict['pathClientSecret']
    SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    STORAGE = Storage(dict['pathTokenDrive'])
    # Fetch credentials from storage
    credentials = STORAGE.get()
    # If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials

def iter_pd(df):
    for val in df.columns:
        yield val
    for row in df.to_numpy():
        for val in row:
            if pd.isna(val):
                yield ""
            else:
                yield val

def pandas_to_sheets(pandas_df, sheet, clear = True):
    # Updates all values in a workbook to match a pandas dataframe
    if clear:
        sheet.clear()
    (row, col) = pandas_df.shape
    cells = sheet.range("A1:{}".format(gspread.utils.rowcol_to_a1(row + 1, col)))
    for cell, val in zip(cells, iter_pd(pandas_df)):
        cell.value = val
    sheet.update_cells(cells)


