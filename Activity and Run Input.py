# CSV Header Date,Type,Time,Piece,Goals,Sections,Tempos,AttemptsTotal,SuccessfulAttempts,UnsuccessfulAttempts,NeutralAttempts,Reflection

# Reference: Documentation on adding lists to DataFrames https://stackoverflow.com/questions/26483254/python-pandas-insert-list-into-a-cell
# FIXME error handling for inputs
# FIXME random encouragements

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
    'Reflection': '',
    'Session': 0,
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
    'Reflection': 'Fill',
    'Session': 0
}

Blank_List = ['Date','Type','Time','Piece','Goals','Sections','Tempos',
              'AttemptsTotal','SuccessfulAttempts','UnsuccessfulAttempts',
              'NeutralAttempts','Reflection','Session']

Notes_Dict = {'quarter':'♩','eigth':'♪','eighth_beamed':"♫",'repeat_left':'𝄆','repeat_right':'𝄇','sixteenth_beamed':'♬'}

print(f"Welcome to {Notes_Dict['repeat_left']} PRACKTICE {Notes_Dict['repeat_right']}, "
      f"the music practicing app! {Notes_Dict['eighth_beamed']}")
print()

def main_menu():

    user_profile = input("What user profile are we using? (Enter anything to navigate to profile creation)"
                         "\nProfile (Case sensitive)> ")

    global creation_value
    global user_csv

    try:

        # create user_csv that all functions will use
        user_csv = str(user_profile) + ".csv"

        # create dataframe
        global dfp
        data = pd.read_csv(user_csv)
        data.head()
        dfp = pd.DataFrame(data)

        print(f"Welcome back {user_profile}!")

        # set creation_value
        creation_value = False

        main_menu_valid(creation_value)

    except FileNotFoundError:

        print("User profile does not exist. Would you like to create a new profile, or retry account input?\n[1] New Profile\n[2] Retry")
        user_choice = input("Choice> ")
        if user_choice == "1":
            account_creation(user_profile)
        elif user_choice == "2":
            main_menu()

# FIXED ERROR HANDLING
def account_creation(user_profile):

    # set a variable for branches if this is a new account
    creation_value = True

    print("What would you like this account to be named?")
    account_name = input("Name> ")
    print()

    # Create new account
    account_csv = account_name + ".csv"
    with open(account_csv, "w") as creating_file:
        creating_writer = csv.writer(creating_file)
        creating_writer.writerow(Blank_List)
    print(f"Welcome to {Notes_Dict['repeat_left']} PRACKTICE {Notes_Dict['repeat_right']}, {account_name}!")

    # delcare user_csv
    user_csv = str(user_profile) + ".csv"

    # assign new dfp dataframe
    global dfp
    data = pd.read_csv(user_csv)
    data.head()
    dfp = pd.DataFrame(data)

    main_menu_valid(creation_value)

# FIXED ERROR HANDLING
def main_menu_valid(value):

    # error handling abstractions
    if value == False:
        user_main_menu = 0
        while user_main_menu != (1 or 2 or 3):
            print("[1] Start a practice session")
            print("[2] Analyze data")
            print('[3] Quit')
            user_main_menu = input("Choice> ")
            if user_main_menu == '1':
                session_start(value)
            elif user_main_menu == '2':
                return 0
            elif user_main_menu == '3':
                print()
            else:
                print("Please enter 1, 2, or 3")
                print()

    if value == True:
        user_main_menu = 0
        while user_main_menu != ('1' or '2'):
            print("[1] Start a practice session")
            user_main_menu = input("Choice> ")
            if user_main_menu == '1':
                session_start(value)
            elif user_main_menu == '2':
                print()
            else:
                print("Please enter either 1 or 2")
                print()

# FIXED ERROR HANDLING
def session_start(value):

    if value == False:
        # FINDS LENGTH OF SESSIONS
        Activity_Dict['Session'] = int(determine_last_session(user_csv) + 1)
        Run_Dict['Session'] = int(determine_last_session(user_csv) + 1)
        # ASKS FOR INPUT (WITH ERROR HANDLING)

        choice = 0
        while choice != ('1' or '2'):
            print("Would you like to see a report of your last session?\n[1] Yes\n[2] No")
            choice = input("Choice> ")
            if choice == "1":
                generate_report_last_session()
                activity_start()
            elif choice == "2":
                activity_start()
            else:
                print("Please select either 1 or 2")

    elif value == True:
        activity_start()

# FIXED
def activity_start():

    print("You started a new activity")
    print()

    # OBTAINING DATE
    date = datetime.date.today()

    date_string = str(date)

    Activity_Dict['Date'] = date_string

    # SETTING TYPE
    Activity_Dict['Type'] = 'Activity'

    # TIME SET AFTER ALL RUNS COMPLETED
    Activity_Dict['Time'] = time.time()

    # SETTING PIECE
    current_piece = piece_retrieval(user_csv)
    Activity_Dict['Piece'] = current_piece

    # SETTING GOALS
    current_goals = input("What are our goals for this activity?> ")

    if len(current_goals) == 0:
        current_goals = 'None'

    Activity_Dict['Goals'] = current_goals

    # REFLECTIONS SET LATER

    print('We will now start an individual run')

    run_start_measures()

# FIXED
def run_start_measures():

    # RESET TO BE APPENDED TO
    Run_Dict['Sections'] = []

    # RUN SECTIONS
    measure_list = []
    start_measure = 'a'
    end_measure = 'a'

    start_measure = error_handling_int("What measure are we starting at?> ",start_measure)

    measure_list.append(start_measure)

    end_measure = error_handling_int("What measure are we ending at?> ",end_measure)

    measure_list.append(end_measure)

    measure_list.sort()

    Run_Dict['Sections'] = measure_list
    print(Run_Dict['Sections'])

    run_start_tempos()

# FIXED
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
    tempo = 'a'
    while type(tempo) != int():
        try:
            tempo = int(input("What tempo are we running this at?> "))
            break
        except ValueError:
            print("Please enter a number")
            print()

    Run_Dict['Tempos'] = tempo
    Activity_Dict['Tempos'].append(tempo)

    candy_tracker(Activity_Dict['Goals'])

# FIXED
def candy_tracker(activity_goal):

    # establish format
    format_string = '{left:<16}{right:>16}'

    # initialize variables
    user_input = 0
    running_total = 0
    TotalAttempts = 0
    SuccessfulAttempts = 0
    UnsuccessfulAttempts = 0
    NeutralAttempts = 0

    difficulty_value = False

    candy_length_dummy = 0

    # error handling input
    while candy_length_dummy != 1:
        candy_length = input("Enter amount of tokens between 1 and 16> ")
        print()
        try:
            if int(candy_length) in range(1,17):
                candy_length_dummy = 1
                candy_length = int(candy_length)
                break
            else:
                print("Please enter a number between 1 and 16\n")
        except ValueError:
            print("Please enter a valid number\n")

    candies_left_standard = Notes_Dict['quarter'] * candy_length

    # error handling for difficulty
    difficulty = error_handling_int_plus(['Yes','No'],
                                         'Would you like to practice where your tokens reset on an unsuccessful run?')

    if difficulty == 1:
        difficulty_value = True

    print(difficulty_value)

    print()

    run_start_practice = time.time()

    # start loop for token tracking
    while user_input != "1":

        if running_total <= 0:
            candies_left = candies_left_standard
            running_total = 0

        elif running_total > candy_length:
            candies_left = candies_left_standard[:(running_total - candy_length)]

        else:
            candies_left = candies_left_standard[:-(running_total - candy_length)]
        candies_right = candies_left_standard[:(candy_length - len(candies_left))]

        print(f"{Notes_Dict['repeat_left']} Activity Goal: {activity_goal} {Notes_Dict['repeat_right']}\n")
        print(format_string.format(left="Left", right="Right"))
        print(format_string.format(left=candies_left, right=candies_right))

        print("\n[1] Exit [2] Successful run [3] Unfocused run [4] Unsuccessful run\n")
        user_input = input("Choice> ")
        if user_input in ['2','3','4']:
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
        else:
            print("Please enter a valid number")

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

    run_testing_frame[0:1].to_csv(user_csv, mode='a', index=False, header=False)

    print("Way to go!")
    print("What would you like to do next?")
    user_option = error_handling_int_plus(["Start a new piece or end session",'Keep running this section at different tempo',
          'Keep running this piece with a different section'],'Option> ')
    if user_option == 1:
        activity_end()
    if user_option == 2:
        run_start_tempos()
    if user_option == 3:
        run_start_measures()


def activity_end():

    # TIME
    act_stop_practice = time.time()
    total_time = act_stop_practice - Activity_Dict['Time']
    Activity_Dict['Time'] = round(total_time, 2)

    # REFLECTION
    act_reflection = input("What are your notes/reflections on the activity you just completed?> ")
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

    act_testing_frame[0:1].to_csv(user_csv, mode='a', index=False, header=False)

    print('What would you like to do next?')
    user_option = error_handling_int_plus(['Start a new piece', 'End session'],'Option> ')

    if user_option == 1:
        activity_start()
    elif user_option == 2:
        main_menu_valid(False)

# BACKGROUND CALLS

def determine_last_session(user_profile):
    dfp = pd.read_csv(user_profile)
    last_index = int(dfp.size / 13) - 1
    last_session = int(dfp.iloc[last_index]['Session'])
    return last_session

def generate_report_last_session():

    #establish empty lists
    activity_indices = []
    run_indices = []

    # cycle to get indices (able to put activities in front of runs)
    for index in list(dfp.index[dfp['Session'] == determine_last_session(user_csv)]):
        if dfp.iloc[index]['Type'] == 'Activity':
            activity_indices.append(index)
        elif dfp.iloc[index]['Type'] == 'Run':
            run_indices.append(index)

    for index in activity_indices:
        if dfp.iloc[index]["Type"] == 'Activity':
            print()
            print(f"Piece: {dfp.iloc[index]['Piece']}")
            print(f"Overall reflection: {dfp.iloc[index]['Reflection']}")
            print(f"Time spent (in minutes): {seconds_to_minutes(dfp.iloc[index]['Time'])}")

        for counter,index in enumerate(run_indices):
            if dfp.iloc[index]["Type"] == 'Run':
                print()
                print(f"\tAction type: {dfp.iloc[index]['Type']}_{counter}")
                print(f"\t\tTempos: {dfp.iloc[index]['Tempos']}")
                print(f"\t\tSections: {dfp.iloc[index]['Sections']}")
                print(f"\t\tReflection: {dfp.iloc[index]['Reflection']}")
                print(f"\t\tTime spent (in minutes): {seconds_to_minutes(dfp.iloc[index]['Time'])}")

    print()

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
        user_piece = input("Activity name> ")
    else:
        user_piece = previous_piece[piece_selection]

    return user_piece

def error_handling_int(message,variable):
    while type(variable) != int():
        try:
            variable = int(input(message))
            break
        except ValueError:
            print()
            print("Please enter a number")
    return variable

def error_handling_int_plus(message_list,message):
    variable_dummy = 0
    while variable_dummy != 1:
        for index, item in enumerate(message_list):
            print(f"[{index + 1}] {message_list[index]}")
        variable = input(message)
        print()
        try:
            if int(variable) in range(1,len(message_list) + 1):
                variable_dummy = 1
                variable = int(variable)
                break
            else:
                print(f"Please enter a number between 1 and {len(message_list)}\n")
        except ValueError:
            print('Please enter a valid number\n')

    return variable

def seconds_to_minutes(seconds):
    just_minutes = seconds // 60
    just_seconds = seconds % 60
    return round((just_minutes + just_seconds/60),1)

run_start_measures()