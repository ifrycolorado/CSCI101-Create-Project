import csv
from datetime import datetime

def candy_tracker():
    candy_length = int(input("Enter amount between 1 and 16> "))

    start_practice = time.time()

    candies_left_standard = "*" * candy_length
    candies_right_standard = ""
    candies_left = ""
    candies_right = ""

    format_string = '{left:<16}{right:>16}'

    user_input = 0
    successes = 0
    attempts = 0

    while user_input != "1":
        print("[1] Exit\n[2] Successful run\n[3] Negation\n[4] Unsuccessful run\n")
        user_input = input("Select choice: ")

        if user_input == "2":
            successes += 1
            print(successes)
        elif user_input == "4":
            successes -= 1
        if successes <= 0:
            candies_left = candies_left_standard
            candies_right = ""
            successes = 0
        elif successes > candy_length:
            candies_left = candies_left = candies_left_standard[:(successes - candy_length)]
        else:
            candies_left = candies_left_standard[:-(successes - candy_length)]
        candies_right = candies_left_standard[:(candy_length - len(candies_left))]

        print(format_string.format(left="Left", right="Right"))
        print(format_string.format(left=candies_left, right=candies_right))
        print()

        attempts += 1

        if successes == candy_length * 2:
            user_input = "1"

    stop_practice = time.time()

    print(f"Length of practice = {stop_practice - start_practice} seconds")
    print(f"Amount of runs = {attempts}")

date = ""
type = ""
time = ""
piece = ""
goals = ""
intent = ""
section = ""
tempo = ""
attemptsTotal = ''
successfulAttempts = ''
unsuccessfulAttempts = ''
neutralAttempts = ''
reflection = ''

master_list = [date,type,time,piece,goals,intent,section,tempo,attemptsTotal,successfulAttempts,
                   unsuccessfulAttempts, neutralAttempts, reflection]

print("[1] Start a new session")
user_input = input("How can we get started today?> ")

# start session
if user_input == "1":

    print("We are starting a session")
    date = datetime.now()
    type = "SessionStart"
    goals = input("What are your goals?> ")
    session_list = [date, type, time, piece, goals, intent, section, tempo, attemptsTotal, successfulAttempts,
                   unsuccessfulAttempts, neutralAttempts, reflection]
    with open('PT.csv', 'a') as PT_file:
        PT_writer = csv.writer(PT_file)
        PT_writer.writerow(master_list)

    #Activity1 inputs

    print('We are now starting a piece activity')
    date = datetime.now()
    type = "Activity1"
    piece = input("What piece are we practicing?> ")
    goals = input('What goals do you have for this piece?> ')
    intent = input('What measures do you want to run?> ')
    section = []
    tempo = []
    attemptsTotal = 0
    successfulAttempts = 0
    unsuccessfulAttempts = 0
    neutralAttempts = 0
    reflection = ""


    activity1_list = [date, type, time, piece, goals, intent, section, tempo, attemptsTotal, successfulAttempts,
                   unsuccessfulAttempts, neutralAttempts, reflection]








