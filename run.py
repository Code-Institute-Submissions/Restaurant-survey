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

    sum_averege = sum(total) / len(total)
    return f"Responses Gatherd, the averege of all answers is: {sum_averege}\n"


def get_averege_of_each_question(sheet):
    """
    Gets the averege for each question to later update the averege sheet
    so that the user can get an overview of the reviews.
    """
    values = []
    for ind in range(2, 12):
        column = sheet.col_values(ind)[1: 11]
        column = list(map(int, column))
        # for lists in column:
        #     averege_for_each = sum(column) / len(column)
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

    new_avereges = ['Doing ok' if i == 3.3 else 'Needs attention' if
                    i == 3.2 else 'Urgent need of attention' if i ==
                    3.1 else 'Critical' if i <= 3.0 else 'Doing Good' for i in avereges]

    return new_avereges


def update_improve_worksheet(data):
    """
    Updates the improve worksheet with
    the values generated in the previous function
    """
    print("\nConverting values so user can se where attention is needed\n")
    improve_sheet = SHEET.worksheet('improve')
    improve_sheet.append_row(data)
    print("Values converted see Google Sheet\n")


def welcome_main_function():
    print("Hello! This program will run all the ratings from a survey and return avereges or see what areas is in need of improvements")
    print("Enter the word 'r' for return avereges' to calculate the avereges of the survey results.")
    print("Or enter the letter 'i' for 'improvement' to see what areas needs to be improved.")
    print("Finally, You can choose 'b' for both of the above.")
    while True:

        user_input = input("Enter here: \n")

        if user_input == "r":
            sum_averege_func = response_values()
            print(sum_averege_func)
            avereges = get_averege_of_each_question(
                SHEET.worksheet('responses'))
            update_averege_worksheet(avereges)
            return
        elif user_input == "i":
            new_avereges = get_most_disliked_area(
                SHEET.worksheet('responses'))
            update_improve_worksheet(new_avereges)
            return
        elif user_input == "b":
            sum_averege_func = response_values()
            print(sum_averege_func)
            avereges = get_averege_of_each_question(
                SHEET.worksheet('responses'))
            update_averege_worksheet(avereges)
            new_avereges = get_most_disliked_area(
                SHEET.worksheet('responses'))
            update_improve_worksheet(new_avereges)
            return
        validate_user_input(user_input)

    return True


def validate_user_input(user_input):
    """
    Validate user input, and keeps the program running until user enters correct value
    """
    try:
        if len(user_input) == 0:
            print("You need to enter something for the program to work")
        elif user_input not in ['r', 'i', 'b']:
            print("Check that you entered the right letter")

    except ValueError as e:
        print(f"Watch out, {e}")

    return True


def main():
    """
    Main function that will run all the other functions
    """
    welcome_main_function()


main()
