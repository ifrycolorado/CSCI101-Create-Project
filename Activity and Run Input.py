# CSV Header Date,Type,Time,Piece,Goals,Sections,Tempos,AttemptsTotal,SuccessfulAttempts,UnsuccessfulAttempts,NeutralAttempts,Reflection

# Reference: Documentation on adding lists to DataFrames https://stackoverflow.com/questions/26483254/python-pandas-insert-list-into-a-cell
#FIXME .csv must be alterable via user_profile

import datetime
import time
import pandas as pd
import csv

Activity_Dict = {
    'Date': '',
    'Type': '',
    'Time': 0,
    'Piece': '',
    'Goals': 'None',
    'Sections': [],
    'Tempos': [],
    'AttemptsTotal': 0,
    'SuccessfulAttempts': 0,
    'UnsuccessfulAttempts': 0,
    'NeutralAttempts': 0,
    'Reflection': ''
}

Run_Dict = {
    'Date': '',
    'Type': '',
    'Time': 0,
    'Piece': '',
    'Goals': 'None',
    'Sections': [],
    'Tempos': 0,
    'AttemptsTotal': 0,
    'SuccessfulAttempts': 0,
    'UnsuccessfulAttempts': 0,
    'NeutralAttempts': 0,
    'Reflection': 'Fill'
}

def activity_start():
    print("You started a new activity")

    # OBTAINING DATE
    # FIXME is it worth keeping it as a datetime object?
    date = datetime.date.today()

    date_string = str(date)

    Activity_Dict['Date'] = date_string

    # SETTING TYPE
    Activity_Dict['Type'] = 'Activity'

    # TIME SET AFTER ALL RUNS COMPLETED
    Activity_Dict['Time'] = time.time()

    # SETTING PIECE
    current_piece = piece_retrieval('Isaac.csv')
    Activity_Dict['Piece'] = current_piece

    # SETTING GOALS
    current_goals = input("What are our goals for this activity?> ")
    Activity_Dict['Goals'] = current_goals

    # REFLECTIONS SET LATER

    print('We will now start an individual run')

    run_start_measures()


def run_start_measures():

    # RESET TO BE APPENDED TO
    Run_Dict['Sections'] = []

    # RUN SECTIONS
    start_measure = int(input("What measure are we starting at?> "))
    end_measure = int(input("What measure are we ending at?> "))
    measure_list = [start_measure, end_measure]

    Run_Dict['Sections'] = measure_list

    run_start_tempos()


def run_start_tempos():

    # DATE
    Run_Dict['Date'] = str(datetime.date.today())

    # TYPE
    Run_Dict['Type'] = 'Run'

    # PIECE
    Run_Dict['Piece'] = Activity_Dict['Piece']

    # ACTIVITY SECTONS
    Activity_Dict['Sections'].append(Run_Dict['Sections'])

    # TEMPOS
    tempo = int(input("What tempo are we running this at?> "))
    Run_Dict['Tempos'] = tempo
    Activity_Dict['Tempos'].append(tempo)

    candy_tracker(Activity_Dict['Goals'])


def candy_tracker(activity_goal):

    format_string = '{left:<16}{right:>16}'

    user_input = 0
    running_total = 0
    TotalAttempts = 0
    SuccessfulAttempts = 0
    UnsuccessfulAttempts = 0
    NeutralAttempts = 0

    difficulty_value = False

    candy_length = int(input("Enter amount of tokens between 1 and 16> "))

    difficulty = int(input("Would you like to practice where your tokens reset on an unsuccessful run?\n[1] Yes\n[2] No\nOption> "))

    candies_left_standard = "*" * candy_length

    if difficulty == 1:
        difficulty_value = True

    print()

    run_start_practice = time.time()

    while user_input != "1":

        if running_total <= 0:
            candies_left = candies_left_standard
            running_total = 0

        elif running_total > candy_length:
            candies_left = candies_left_standard[:(running_total - candy_length)]

        else:
            candies_left = candies_left_standard[:-(running_total - candy_length)]
        candies_right = candies_left_standard[:(candy_length - len(candies_left))]

        print(f"Activity Goal: {activity_goal}")
        print(format_string.format(left="Left", right="Right"))
        print(format_string.format(left=candies_left, right=candies_right))

        print("[1] Exit\n[2] Successful run\n[3] Negation\n[4] Unsuccessful run\n")
        user_input = input("Select choice: ")

        if user_input == "2":
            running_total += 1
            SuccessfulAttempts += 1

        elif user_input == "3":
            NeutralAttempts += 1

        elif user_input == "4":
            UnsuccessfulAttempts += 1
            if difficulty_value == True:
                running_total = 0
            else:
                running_total -= 1

        TotalAttempts += 1

        if running_total == candy_length * 2:
            user_input = "1"

    # TIME
    run_stop_practice = time.time()
    Run_Dict['Time'] = round((run_stop_practice - run_start_practice), 2)

    # ATTEMPTS
    Run_Dict['AttemptsTotal'] = TotalAttempts
    Activity_Dict['AttemptsTotal'] += TotalAttempts

    Run_Dict['SuccessfulAttempts'] = SuccessfulAttempts
    Activity_Dict['SuccessfulAttempts'] += SuccessfulAttempts

    Run_Dict['UnsuccessfulAttempts'] = UnsuccessfulAttempts
    Activity_Dict['UnsuccessfulAttempts'] += UnsuccessfulAttempts

    Run_Dict['NeutralAttempts'] = NeutralAttempts
    Activity_Dict['NeutralAttempts'] += NeutralAttempts

    print(f" Total Attempts: {TotalAttempts}")
    print(f' Successful Attempts: {SuccessfulAttempts}')

    print(f"Total Time in Seconds: {(run_stop_practice - run_start_practice):.2f}")

    # REFLECTION
    run_reflection = input("Any thoughts on that run? (Press enter to bypass)> ")
    if len(run_reflection) == 0:
        run_reflection = "None"
    Run_Dict['Reflection'] = run_reflection

    from_run_to_session()


def from_run_to_session():

    # APPEND TO CSV
    run_testing_frame = pd.DataFrame(Run_Dict)

    dummy_sections = Run_Dict['Sections']
    dummy_tempos = Run_Dict['Tempos']
    run_testing_frame['Sections'] = run_testing_frame['Sections'].astype('object')
    run_testing_frame['Tempos'] = run_testing_frame['Tempos'].astype('object')

    run_testing_frame.at[0, "Sections"] = dummy_sections
    run_testing_frame.at[0, "Tempos"] = dummy_tempos

    run_testing_frame[0:1].to_csv('Isaac.csv', mode='a', index=False, header=False)

    print("Way to go!")
    print("What would you like to do next?")
    print("[1] Start a new piece\n[2] Keep running this section at different tempo\n"
          "[3] Keep running this piece with a different section")
    user_option = int(input("OPTION> "))
    if user_option == 1:
        print('Kicked back to activity manager, start reflection')
        activity_end()
    if user_option == 2:
        run_start_tempos()
    if user_option == 3:
        run_start_measures()

def data_call(user_profile):
    pt_table = pd.read_csv(user_profile)
    user_type = input("What type would you like to retrieve? (Either Activity or Run)> ")
    type_frame = pt_table['Type'] == user_type
    type_indices = list(pt_table.index[type_frame])
    for index in type_indices:
        print(pt_table.iloc[index])


def activity_end():

    # TIME
    act_stop_practice = time.time()
    total_time = act_stop_practice - Activity_Dict['Time']
    Activity_Dict['Time'] = round(total_time, 2)

    # REFLECTION
    act_reflection = input("What are your notes/reflections on that activity?> ")
    if len(act_reflection) == 0:
        act_reflection = "None"
    Activity_Dict['Reflection'] = act_reflection

    # ADD TO CSV
    act_testing_frame = pd.DataFrame(Activity_Dict)

    dummy_sections = Activity_Dict['Sections']
    dummy_tempos = Activity_Dict['Tempos']

    act_testing_frame['Sections'] = act_testing_frame['Sections'].astype('object')
    act_testing_frame['Tempos'] = act_testing_frame['Tempos'].astype('object')

    act_testing_frame.at[0, "Sections"] = dummy_sections
    act_testing_frame.at[0, "Tempos"] = dummy_tempos

    print(act_testing_frame.iloc[0])
    print(act_testing_frame[0:1])

    act_testing_frame[0:1].to_csv('Isaac.csv', mode='a', index=False, header=False)

    print("Way to practice that piece!")
    print('What would you like to do next?')
    print("[1] Start a new piece\n[2] End session")
    print("[DEV3] End trial and print")
    user_option = int(input("OPTION> "))

    if user_option == 1:
        activity_start()
    elif user_option == 2:
        print("Kicked to end of session manager")
    elif user_option == 3:
        print(Activity_Dict)
        print(Run_Dict)
    else:
        print("Please enter a valid number")

def main_menu():

    #FIXME Maybe some art?
    print("Welcome to Pracktice, the music practicing app!")

    global user_csv

    user_profile = input("What user profile are we using?")
    user_csv = str(user_profile) + ".csv"
    print(f"Welcome back {user_profile}!")

    print("[1] Start a practice session")
    print("[2] Analyze data")
    user_main_menu = int(input("Choice> "))
    if user_main_menu == 1:
        activity_start()
    elif user_main_menu == 2:
        data_call(user_profile)


def piece_retrieval(user_csv):

    print("Please select an activity or piece")

    previous_piece = []

    with open(user_csv, "r") as user_csv_file:
        user_csv_reader = csv.reader(user_csv_file)
        for line in user_csv_reader:
            if line[1] == "Activity":
                if line[3] not in previous_piece:
                    previous_piece.append(line[3])

    for index,piece in enumerate(previous_piece):
        print(f"[{index}] {piece}")
    print(f"[{len(previous_piece)}] Define a new activity")

    try:
        piece_selection = int(input("Selection> "))
    except (TypeError, ValueError, IndexError):
        print("Please enter a valid number")

    #FIXME Error Handling
    if piece_selection == len(previous_piece):
        user_piece = input("Activity name")
    else:
        user_piece = previous_piece[piece_selection]

    return user_piece

activity_start()