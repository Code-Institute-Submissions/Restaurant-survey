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


def update_averege_worksheet(data):
    """
    Updates the Averege worksheet with the data generated in the previous function
    """

    print("Calculating Avereges\n")

    averege_sheet = SHEET.worksheet('averege')
    averege_sheet.append_row(data)

    print("Avereges Calculated, See Avereges form in Google sheets!\n")


def get_most_disliked_area(sheet):
    """
    Gathers which of the areas are most disliked
    """

    avereges = []
    for ind in range(2, 12):
        column = sheet.col_values(ind)[1: 11]
        column = list(map(int, column))
        for lists in column:
            averege_for_each = sum(column) / len(column)

        avereges.append(averege_for_each)
    new_avereges = avereges.pop()
    print(new_avereges)
    new_avereges = ['Doing ok' if i ==
                    3.3 else 'Needs attention' if i == 3.2 else 'Urgent need of attention' if i == 3.1 else 'Critical' if i <= 3.0 else 'Doing Good' for i in avereges]

    return new_avereges


# this is data for update
new_avereges = get_most_disliked_area(SHEET.worksheet('responses'))
print(new_avereges)


def update_improve_worksheet(data):
    """
    Updates the improve worksheet with the values generated in the previous function
    """
    print("Converting values so user can se where attention is needed")
    improve_sheet = SHEET.worksheet('improve')
    improve_sheet.append_row(data)
    print("Values converted see Google Sheet")


def main():
    """
    A main function that runs all the needed functions for the program to function.
    """

    response_values()
    avereges = get_averege_of_each_question(SHEET.worksheet('responses'))
    update_averege_worksheet(avereges)
    new_avereges = get_most_disliked_area(SHEET.worksheet('responses'))
    update_improve_worksheet(new_avereges)


main()

"""
def welcome_function():
    print("Hello! This program will run all the ratings from a survey and return avereges, aslong with most liked and most disliked subjects.")
    print("What would you like to know, see the options below:")
    print("* total-averege")
    print("* averege-for-each-question")
    print("* most-liekd")
    print("* most-disliked")
    print("** type excatly like above")
    user_input = input("Type your request here: ")

    if user_input == "total-averege":
        response_values()
    elif user_input == "averege-for-each-question":
        get_averege_of_each_question(results)
    elif user_input == "most-liked"
"""
