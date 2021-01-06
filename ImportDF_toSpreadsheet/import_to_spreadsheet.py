import gspread
import lib_gspread as lib

credentials = lib.authorize_credentials(cred)
gc = gspread.authorize(credentials)
id_source = gc.open_by_key("id-speadsheet")
lib.pandas_to_sheets(results, id_source.worksheet("results"))