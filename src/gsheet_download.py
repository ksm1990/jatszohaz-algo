from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
from src.constants import *


def initialize_gspread(service_account_file_path: str):
    credentials = Credentials.from_service_account_file(
        service_account_file_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    return gspread.authorize(credentials)


def sheet_to_df(sheet: gspread.Spreadsheet, worksheet_id: int | str):
    data = sheet.get_worksheet_by_id(worksheet_id).get_values()
    return pd.DataFrame(data[1:], columns=data[0])


def download_data():
    gc = initialize_gspread(CREDENTIALS_FILENAME)
    sheet = gc.open_by_key(MASTER_SHEET_ID)
    beo_df = sheet_to_df(sheet, BEO_WORKSHEET_ID)
    kimittud_df = sheet_to_df(sheet, KIMITTUD_WORKSHEET_ID)
    return beo_df, kimittud_df
