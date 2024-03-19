import gspread
import csv
import urllib
from urllib import request
from google.oauth2.service_account import Credentials
import datetime
import pandas as pd
from urllib.request import urlopen
from io import StringIO

today = datetime.date.today()
csv_file_name = 'kimittud_{}.csv'.format(today)
names = ['ÁDÁM','ALEX','BALU','BELLA','BORCSA','BORI','DÁVID','DORINA','DORKA','EMMA',
         'FANNI','GERGŐ','JANKA','KATA','KRISTÓF','LILLA','MÁRK','NIKI','PANKA','RÉKA',
         'SANYI','SÁRI','TAKI','VANDA','VERONKA']
uniformity_table = pd.DataFrame()

def downloadSheets():
# Define the scope and credentials
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file('nodal-wall-416914-5876acf16f70.json', scopes=scope)
    # Authorize access to Google Sheets
    client = gspread.authorize(credentials)
    # Open the Google Sheet by its URL or title
    sheet = client.open_by_url(
        'https://docs.google.com/spreadsheets/d/1fwhZxPtuP2MSBkTXJRSH-plXGV42mF-HlQPf4KSpFwE/edit#gid=858480548')
    # Replace 'your_sheet_url' with the URL of your Google Sheet
    # Select the worksheet by its index or title
    worksheet = sheet.get_worksheet(1)  # Replace '0' with the index of the worksheet (0-based)
    data = worksheet.get_all_values()
    # Retrieve all values from the worksheet
    # Write the data to a CSV file
    with open(csv_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    print(f"CSV file '{csv_file_name}' saved successfully!")

def CreateUniformityTable():
    df = pd.read_csv(csv_file_name, encoding='ISO-8859-1')
    df.drop(df.columns[[0,1,2,3,4,5,6,7,8,9]], axis=1, inplace=True)
    #delete empty rows:
    column_to_check = 'ÁDÁM'
    df.dropna(subset=column_to_check, inplace=True)
    # print(df.iloc[:,27])
    # SOROK MIN SZÁMA: 2
    # SOROK MAX SZÁMA: 236
    # OSZLOPOK MIN SZÁMA: 0
    # OSZLOPOK MAX SZÁMA: 28
    # df.iloc[SORSZÁM 0-tól indexelve, OSZLOPSZÁM 0-tól indexelve]
    for i in range(0,25): # minden ember oszlopa
        for j in range(1,25-i): # minden ember oszlopát minden másikéval
            uniformity_counter = 0
            uniformity_percentage = 0
            for k in range(2,235):
                # print(df.iloc[k],df.iloc[i])
                if (int(df.iloc[k,i]) + int(df.iloc[k,(i+j)]) == 4):
                    uniformity_counter = uniformity_counter + 1
            # print(df.columns[i] + " - " + df.columns[i+j])
            # print(uniformity_counter)
            uniformity_percentage = (uniformity_counter/234)*100
            # print(uniformity_percentage)
            uniformity_table.loc[df.columns[i],df.columns[i+j]] = uniformity_percentage
    print(uniformity_table)
    uniformity_table.to_csv('uniformity_table.csv')
    return df

# downloadSheets()
CreateUniformityTable()
