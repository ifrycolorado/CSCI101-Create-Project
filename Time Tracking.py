import time
from datetime import datetime

Activity_Dict = {
    'Date': '',
    'Type': '',
    'Time': 0,
    'Piece': '',
    'Goals': '',
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
    'Goals': '',
    'Section': [],
    'Tempo': 0,
    'AttemptsTotal': 0,
    'SuccessfulAttempts': 0,
    'UnsuccessfulAttempts': 0,
    'NeutralAttempts': 0,
    'Reflection': ''
}

def run_start_measures():


    start_measure = int(input("What measure are we starting at?> "))
    end_measure = int(input("What measure are we ending at?> "))
    measure_list = [start_measure, end_measure]
    Run_Dict['Section'] = measure_list
    Activity_Dict['Sections'].append(measure_list)

    run_start_tempos()

def run_start_tempos():

    tempo = int(input("What tempo are we running this at?> "))
    Run_Dict['Tempo'] = tempo
    Activity_Dict['Tempos'].append(tempo)

    candy_tracker()

def candy_tracker():

    format_string = '{left:<16}{right:>16}'

    user_input = 0
    running_total = 0
    TotalAttempts = 0
    SuccessfulAttempts = 0
    UnsuccessfulAttempts = 0
    NeutralAttempts = 0

    difficulty_value = False

    candy_length = int(input("Enter amount between 1 and 16 for candy> "))

    difficulty = int(input("Would you like to practice where your candies reset on an unsuccessful run?\n[1] Yes\n[2] No\nOption> "))

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

        print(format_string.format(left="Left", right="Right"))
        print(format_string.format(left=candies_left, right=candies_right))
        print(running_total)

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
    print(Run_Dict)
    print(Activity_Dict)
    print("Way to go!")
    print("What would you like to do next?")
    print("[1] Start a new piece\n [2] Keep running this section at different tempo\n"
          "[3] Keep running this piece with a different section\n[4] End session")
    user_option = int(input("OPTION> "))
    if user_option == 1:
        print('Kicked back to activity manager, start reflection')
        # FIXME kick to activity manager and force reflection
    if user_option == 2:
        run_start_tempos()
    if user_option == 3:
        run_start_measures()
    if user_option == 3:
        print('Kicked to end of session manager, start Act reflection and Session reflection')
        activity_end()
        # FIXME kick to session manager and force both reflections

run_start_measures()