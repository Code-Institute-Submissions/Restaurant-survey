import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


# Taken from the walkthrough project
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('restaurant_survey')

results = SHEET.worksheet('responses')


def welcome_function():

    # function to get values


def response_values():
    """
    Get the ratings from the responses spreadsheet and
    append them to a variable
    """
    print("\nGathering responses from spreadsheet, standby...\n")
    ratings = SHEET.worksheet('responses').get_all_values()
    responses = ratings[1: -1]
    total = []
    for row in responses:
        rows = row[1: 11]
        for num in rows:
            to_int = int(num)
            total.append(to_int)

    averege = sum(total) / len(total)

    print(f"Responses Gatherd, the averege of all answers is: {averege}\n")


response_values()


def get_averege_of_each_question(sheet):
    """
    Gets the averege for each question to later update the averege sheet
    so that the user can get an overview of the reviews.
    """
    values = []
    for ind in range(2, 12):
        column = sheet.col_values(ind)[1: 11]
        column = list(map(int, column))
        for lists in column:
            averege_for_each = sum(column) / len(column)

        values.append(averege_for_each)
    return values


each_averege = get_averege_of_each_question(results)


def update_averege_worksheet():
    """
    Updates the Averege worksheet with the data generated in the previous function
    """

    print("Calculating Avereges")

    averege_sheet = SHEET.worksheet('averege')
    averege_sheet.append_row(each_averege)

    print("Avereges Calculated, See Avereges form in Google sheets!")


update_averege_worksheet()


def get_most_disliked_area():
    """
    Gathers which of the areas are most disliked
    """


def update_improve_worksheet():
    """
    Updates the improve worksheet with the values generated in the previous function
    """


def get_most_liked():
    """
    Gets the most liked areas of the survey
    """


def update_most_liked_worksheet():
    """
    Updates the most_liked worksheet with the values from the previous worksheet
    """
