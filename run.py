import gspread
from google.oauth2.service_account import Credentials

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
    Get the ratings from the responses spreadsheet and append them to a variable
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


def get_averege_of_each_question():
    """
    Gets the averege for each question to later update the averege sheet 
    so that the user can get an overview of the reviews.
    """


def update_averege_worksheet():
    """
    Updates the Averege worksheet with the data generated in the previous function
    """


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
