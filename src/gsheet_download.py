from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
from src.constants import *
import os
import json
from dotenv import load_dotenv


def initialize_gspread():
    load_dotenv()
    credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_json:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS in env is not set")
    try:
        credentials_info = json.loads(credentials_json)
    except json.JSONDecodeError:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS is not a valid JSON: " + credentials_json
        )
    credentials = Credentials.from_service_account_info(
        credentials_info,
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    return gspread.authorize(credentials)


def sheet_to_df(sheet: gspread.Spreadsheet, worksheet_id: int | str):
    data = sheet.get_worksheet_by_id(worksheet_id).get_values()
    return pd.DataFrame(data[1:], columns=data[0])


def download_data():
    gc = initialize_gspread()
    sheet = gc.open_by_key(MASTER_SHEET_ID)
    beo_df = sheet_to_df(sheet, BEO_WORKSHEET_ID)
    kimittud_df = sheet_to_df(sheet, KIMITTUD_WORKSHEET_ID)
    return beo_df, kimittud_df
