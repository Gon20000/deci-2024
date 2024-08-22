from input import getChoices, getDate, handleSignUpQuestions, handleLogin
from db import addSession, init, addCoach, addAthlete, removeSession


con = init()


def destruct():
    con.close()


print("Do you want to sign up or log in?")
register = getChoices(["Sign up", "Log in"]) == "Sign up"

print("Are you a life coach or an athlete?")
coaching = getChoices(["Life coach", "Athlete"]) == "Life coach"

# Get introductory info from json file in case of sign up
if register:
    inputData = handleSignUpQuestions(coaching)

    id = (addCoach(inputData) if coaching else addAthlete(inputData))[0]
    print(f"Thanks, your ID is {id}. You may use it for future logins!")
elif coaching:
    id, name, *_ = handleLogin(coaching)
    print(f"Welcome, Coach {name}!")
    print("Do you want to add, list or remove sessions?")
    choice = getChoices(["Add", "List", "Remove"]) == "Add"

    date = getDate()
    if date and choice == "Add":
        added = addSession(date, id)
        if added:
            print(f"Successfully added a session with the date {date}")
        else:
            print("A session with this date already exists!")
    elif date and choice == "Remove":
        removed = removeSession(date, id)
        if removed:
            print(f"Successfully removed the session with the date {date}.")
        else:
            print("No session was found with this date!")
else:
    print(coaching)
    name = handleLogin(coaching)
    print(f"Welcome, Athlete {name}!")


destruct()
