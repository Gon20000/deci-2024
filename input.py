import json
import re

from db import selectRecord


def getInt(low, high):
    answer = 0

    while True:
        try:
            answer = int(
                input(
                    "Enter a number inclusively between {} and {}: ".format(
                        low,
                        high)))
        except ValueError:
            print("Invalid number!")
        else:
            break

    return getInt(low, high) if answer < low or answer > high else answer


def getChoices(choices):
    last = len(choices)

    for i in range(last):
        print("{}: {}".format(i + 1, choices[i]))

    return choices[getInt(1, last) - 1]


def getDate():
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    while True:
        date_str = input("Please enter a date (YYYY-MM-DD): ")

        # Validate the format
        if date_pattern.match(date_str):
            # Additional check for valid date values
            try:
                year, month, day = map(int, date_str.split('-'))

                # Check if the date is valid
                if (year == 2024 or year == 2025) and (
                        1 <= month <= 12) and (1 <= day <= 31):
                    # Further checks for days in month could be added here
                    return date_str
                else:
                    print(
                        "Invalid date. Please ensure the month is between 01 and 12, and day is between 01 and 31.")
            except ValueError:
                print("Invalid date. Please ensure the date is in YYYY-MM-DD format.")
        else:
            print("Invalid format. Please use YYYY-MM-DD format.")
        return ""


def handleSignUpQuestions(coaching):
    # Get file contents
    f = json.load(open("./questions.json"))
    inputData = []

    # Select data based on whether the user is an athlete or a life coach
    data = f.get("coach" if coaching else "athlete")
    for entry in data:
        ans = ""
        print(entry.get("question"))

        if entry.get("choices"):
            ans = getChoices(entry.get("choices"))
        elif entry.get("low"):
            ans = getInt(entry.get("low"), entry.get("high"))
        else:
            ans = input()

        inputData.append(ans)

    return inputData


def handleLogin(coaching):
    id = input("Please enter your ID to log in: ")
    while not id.isnumeric():
        id = input("Please enter a valid ID to log in: ")

    data = selectRecord(coaching, id)

    if data is None:
        print("This ID doesn't exist!")
        return handleLogin(coaching)

    return data
