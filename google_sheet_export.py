import gspread
import csv
from google.oauth2.service_account import Credentials
import datetime
import pandas as pd
from itertools import combinations

today = datetime.date.today()
csv_file_name = "kimittud_{}.csv".format(today)
names = [
    "ÁDÁM",
    "ALEX",
    "BALU",
    "BELLA",
    "BORCSA",
    "BORI",
    "DÁVID",
    "DORINA",
    "DORKA",
    "EMMA",
    "FANNI",
    "GERGŐ",
    "JANKA",
    "KATA",
    "KRISTÓF",
    "LILLA",
    "MÁRK",
    "NIKI",
    "PANKA",
    "RÉKA",
    "SANYI",
    "SÁRI",
    "TAKI",
    "VANDA",
    "VERONKA",
]
uniformity_table = pd.DataFrame()
processed_name = csv_file_name + "-processed" + ".csv"
list_of_applicants = [
    "ÁDÁM",
    "ALEX",
    "BALU",
    "BELLA",
    "BORCSA",
    "BORI",
    "DÁVID",
    "DORINA",
    "DORKA",
    "EMMA",
]
date = "2024-04-22"
credentials_filename = "nodal-wall-416914-5876acf16f70.json"
beo_worksheet_id = 2121169814
kimittud_worksheet_id = 858480548
sheet_id = "1fwhZxPtuP2MSBkTXJRSH-plXGV42mF-HlQPf4KSpFwE"


def initialize_gspread(service_account_file_path: str):
    credentials = Credentials.from_service_account_file(
        service_account_file_path, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return gspread.authorize(credentials)


def google_worksheet_to_df(sheet_id: str, worksheet_id: str | int):
    client = initialize_gspread(credentials_filename)
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.get_worksheet_by_id(worksheet_id)
    data = worksheet.get_all_values()
    return pd.DataFrame(data[1:], columns=data[0])


def get_beosztas_df():
    return google_worksheet_to_df(sheet_id, beo_worksheet_id)

def get_kimittud_df():
    return google_worksheet_to_df(sheet_id, kimittud_worksheet_id)

def process_beo_df(beo_df: pd.DataFrame): 
    beo_df.drop(beo_df.columns[[0, 1, 3, 4, 5, 6, 7, 8, 9, -1]], axis=1, inplace=True)
    beo_df.dropna(subset="ÁDÁM", inplace=True)

def DownloadSheets():

    client = initialize_gspread("nodal-wall-416914-5876acf16f70.json")
    # Open the Google Sheet by its URL or title
    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1fwhZxPtuP2MSBkTXJRSH-plXGV42mF-HlQPf4KSpFwE/edit#gid=858480548"
    )

    worksheet = sheet.get_worksheet(
        1
    )  # Replace '0' with the index of the worksheet (0-based)
    data = worksheet.get_all_values()
    # Retrieve all values from the worksheet
    # Write the data to a CSV file
    with open(csv_file_name, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    print(f"CSV file '{csv_file_name}' saved successfully!")


def ProcessCSV():
    df = pd.read_csv(csv_file_name, encoding="ISO-8859-1")
    # df = pd.read_csv(csv_file_name)
    df.drop(df.columns[[0, 1, 3, 4, 5, 6, 7, 8, 9, -1]], axis=1, inplace=True)
    # delete empty rows based on the last value of column 'ÁDÁM':
    column_to_check = "ÁDÁM"
    df.dropna(subset=column_to_check, inplace=True)
    df.to_csv(processed_name)


def CreateUniformityTable():
    # df = pd.read_csv(processed_name, encoding='ISO-8859-1')
    df = pd.read_csv(processed_name)
    # df.drop(df.columns[[0,1,2,3,4,5,6,7,8,9]], axis=1, inplace=True)
    # #delete empty rows:
    # column_to_check = 'ÁDÁM'
    # df.dropna(subset=column_to_check, inplace=True)
    # print(df.iloc[:,27])
    # SOROK MIN SZÁMA: 2
    # SOROK MAX SZÁMA: 236
    # OSZLOPOK MIN SZÁMA: 0
    # OSZLOPOK MAX SZÁMA: 28
    # df.iloc[SORSZÁM 0-tól indexelve, OSZLOPSZÁM 0-tól indexelve]
    for i in range(0, 25):  # minden ember oszlopa
        for j in range(1, 25 - i):  # minden ember oszlopát minden másikéval
            uniformity_counter = 0
            uniformity_percentage = 0
            for k in range(2, 235):
                # print(df.iloc[k],df.iloc[i])
                if int(df.iloc[k, i]) + int(df.iloc[k, (i + j)]) == 4:
                    uniformity_counter = uniformity_counter + 1
            # print(df.columns[i] + " - " + df.columns[i+j])
            # print(uniformity_counter)
            uniformity_percentage = (uniformity_counter / 234) * 100
            # print(uniformity_percentage)
            uniformity_table.loc[df.columns[i], df.columns[i + j]] = (
                uniformity_percentage
            )
    print(uniformity_table)
    uniformity_table.to_csv("uniformity_table.csv")
    return df


# input: (number of gamemasters for the event, list of gamemasters applying for an event)
def GenerateMasterDatabase(
    number_of_gamemasters: int, list_of_applicants: list[str], date
):
    variations_database = pd.read_csv(processed_name)
    # print(variations_database)
    # drop unnecessary columns: last 4 and first
    variations_database.drop(
        variations_database.columns[[0, -1, -2, -3, -4]], axis=1, inplace=True
    )
    # variations_database.drop(variations_database.index[0], inplace=True)
    # variations_database.drop(variations_database.index[0], inplace=True)
    # dataframe info:
    # variations_database.info()
    # print(variations_database.shape)
    # print("no-of-columns: ")
    # print(len(variations_database.columns))
    # print(variations_database)
    # print(variations_database)
    # number of applicants per pillanat az összes létező játékmester (kb. 25 ember), de át kell írni a jelentkezők listájára
    # number_of_applicants = len(variations_database.columns)-1 # az első oszlop a játék oszlop
    # print(len(variations_database))
    combination_list_of_gamemasters = list(
        combinations(list_of_applicants, number_of_gamemasters)
    )
    # print(combination_list_of_gamemasters)
    # print(len(combination_list_of_gamemasters))
    # print(len(list_of_applicants))
    # print(combination_list_of_gamemasters[15]) # 15. variáció
    # print(variations_database.iloc[:,12]) # 12. oszlopa a kimittudnak
    # a kimittud adott névhez tartozó sorszám oszlopa:
    # print(variations_database.iloc[:,10])
    # print(variations_database.iloc[10,:])
    # a kimittud adott névhez tartozó oszlopa:
    # print(variations_database["BORCSA"])
    # max = len(combination_list_of_gamemasters)
    # print(max)
    count = 0
    dict_of_results = {}
    # create external file for results
    # dirname = os.path.dirname(__file__)
    # new_folder = "{}-variations".format(date)
    # path = os.path.join(dirname,new_folder)
    # os.mkdir(path)
    for comb in combination_list_of_gamemasters:
        count += 1
        number_of_games_over_57percent = 0
        list_of_games_over_57percent = []
        comb_evaluation_dataframe = pd.DataFrame()
        for i in range(0, number_of_gamemasters):
            comb_evaluation_dataframe[comb[i]] = variations_database[comb[i]]
            # comb_evaluation_dataframe[comb[i]] = variations_database.iloc[:, comb[i]]
        for j in range(2, len(comb_evaluation_dataframe)):
            gamemasters_with_2_of_given_game = 0
            for k in range(0, number_of_gamemasters):
                # print(comb_evaluation_dataframe.iloc[k,j])
                if int(comb_evaluation_dataframe.iloc[j, k]) == 2:
                    gamemasters_with_2_of_given_game += 1
            # print(gamemasters_with_2_of_given_game)
            if gamemasters_with_2_of_given_game > 3:
                # list_of_games_over_57percent.append(variations_database[j])
                list_of_games_over_57percent.append(
                    str(j) + " - " + str(variations_database.iloc[j, 0])
                )
                number_of_games_over_57percent += 1
        # print(str(number_of_games_over_57percent) + " - " + str(list(comb)) + "\n")
        # print(list(list_of_games_over_57percent), "\n")
        dict_of_results[comb] = (
            number_of_games_over_57percent,
            list_of_games_over_57percent,
        )
    return dict_of_results


def showTop10(result_dictionary):
    sorted_result_dictionary = sorted(
        result_dictionary.items(), key=lambda x: x[1], reverse=True
    )
    results = sorted_result_dictionary[:10]
    for position, (key, value) in enumerate(results, start=1):
        print(f"{position}, {key}, {value}")
    return results


if __name__ == "__main__":
    # results_dictionary = GenerateMasterDatabase(6, list_of_applicants, date)
    # showTop10(results_dictionary)

    beo_df = get_beosztas_df()
    print(beo_df)

# DownloadSheets()
# ProcessCSV()
# CreateUniformityTable()


# :hatching_chick: Szívesen pakolok oda
# :egg: Ha kell, akkor pakolok oda
# :panda_face: Szeretnék játékmesterkedni
# :derelict_house_building: Ha kell, akkor pakolok vissza
# :bat: Szívesen pakolok vissza
# :lion_face: Leszek főnök
# :key: Lesz nálam kulcs
# :kangaroo: Ot leszek a helyszínen, ha kell, akkor beugrok
# :unicorn_face: Ott leszek játszani, ha nagyon muszáj, akkor beállok
