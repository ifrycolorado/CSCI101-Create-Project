import datetime
import time
import pandas as pd
import csv
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from datetime import date
import random

random_date_list = ['2021-11-27','2021-11-30','2021-12-01','2021-12-03','2021-12-05']
random_piece_list = ['Astral Dance (Stout)','Wilcoxon #52','Warming up','Scales','Strive (Trevino)','Prelude 3 (Bach)']
random_goal_list = ['Increase tone throughout','Develop coordination in left hand','Enjoy and relax','Refine technique',
                    'Practice performing','Have fun','Increase stick height','Play through peice and map','Refrain from giving up',
                    'Develop appreciation for classical music','Prepare auditions']

random_run_reflection_list = ['Pain occurring in left hand, stretch more','This section felt good','Peaking strain at tempo, work on technique',
                              'Missed time signature multiple times, watch counting','Current key signature was difficult, practice this scale more',
                              'This new section was difficult, map beforehand','Refrain from getting excited',
                              'I wish this was easier','Finally made progress, keep tempo up next time',
                              'Ask my director about this part, definitely confusing',
                              'I really should practice more']

random_activity_reflection_list = ['This piece felt good overall','Watch out for the middle section, warm up more beforehand',
                                   'Watch the time signature changes throughout','Whoops, I forgot to practice',
                                   'Lesson instructor said to run this piece more, especially in these tempos',
                                   'Do not freak out, you will get this eventually',
                                   'Definitely feeling better, but watch left hand technique',
                                   'Section leader reminded me that this fails to work',
                                   'I wish there was more musical markings, go back and add in more phrasings',
                                   'These techniques are difficult, go back and count through entire piece']

this_date = '2021-12-05'

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

def determine_last_session(user_profile):
    dfp = pd.read_csv(user_profile)
    last_index = int(dfp.size / 13) - 1
    last_session = int(dfp.iloc[last_index]['Session'])
    return last_session

global creation_value
global user_csv


# create user_csv that all functions will use
user_csv = 'Example.csv'

# create dataframe
global dfp
data = pd.read_csv(user_csv)
data.head()
dfp = pd.DataFrame(data)

def session_start(value):

    if value == False:
        # FINDS LENGTH OF SESSIONS
        Activity_Dict['Session'] = int(determine_last_session(user_csv) + 1)
        Run_Dict['Session'] = int(determine_last_session(user_csv) + 1)
        # ASKS FOR INPUT (WITH ERROR HANDLING)
        activity_start()

    elif value == True:
        activity_start()

def activity_start():

    print("You started a new activity")
    print()

    # OBTAINING DATE
    date_string = random_date_list[random.randint(0,4)]

    Activity_Dict['Date'] = this_date

    # SETTING TYPE
    Activity_Dict['Type'] = 'Activity'

    # SETTING PIECE
    current_piece = random_piece_list[random.randint(0,len(random_piece_list)-1)]
    Activity_Dict['Piece'] = current_piece

    # SETTING GOALS
    current_goals = random_goal_list[random.randint(0,len(random_goal_list)-1)]

    Activity_Dict['Goals'] = current_goals

    # REFLECTIONS SET LATER

    print('We will now start an individual run')

    run_start_measures()

def run_start_measures():

    # RESET TO BE APPENDED TO
    Run_Dict['Sections'] = []

    # RUN SECTIONS
    measure_list = []

    start_measure = random.randint(0,250)

    measure_list.append(start_measure)

    end_measure = random.randint(1,300)

    measure_list.append(end_measure)

    measure_list.sort()

    Run_Dict['Sections'] = measure_list

    run_start_tempos()

def run_start_tempos():

    # DATE
    Run_Dict['Date'] = Activity_Dict['Date']

    # TYPE
    Run_Dict['Type'] = 'Run'

    # PIECE
    Run_Dict['Piece'] = Activity_Dict['Piece']

    # ACTIVITY SECTONS
    Activity_Dict['Sections'].append(Run_Dict['Sections'])

    # TEMPOS
    tempo = random.randint(40,160)

    Run_Dict['Tempos'] = tempo
    Activity_Dict['Tempos'].append(tempo)

    candy_tracker(Activity_Dict['Goals'])

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
    candy_length = random.randint(1,15)

    while user_input != '1':
        user_input = str(random.randint(1,4))

        if user_input == "2":
            running_total += 1
            SuccessfulAttempts += 1

        elif user_input == "3":
            NeutralAttempts += 1

        elif user_input == "4":
            UnsuccessfulAttempts += 1

        TotalAttempts += 1

        if running_total == candy_length * 2:
            user_input = "1"

    # TIME
    run_stop_practice = time.time()
    Run_Dict['Time'] = random.randint(180,600)
    Activity_Dict['Time'] += Run_Dict['Time']

    # ATTEMPTS
    Run_Dict['AttemptsTotal'] = TotalAttempts
    Activity_Dict['AttemptsTotal'] += TotalAttempts

    Run_Dict['SuccessfulAttempts'] = SuccessfulAttempts
    Activity_Dict['SuccessfulAttempts'] += SuccessfulAttempts

    Run_Dict['UnsuccessfulAttempts'] = UnsuccessfulAttempts
    Activity_Dict['UnsuccessfulAttempts'] += UnsuccessfulAttempts

    Run_Dict['NeutralAttempts'] = NeutralAttempts
    Activity_Dict['NeutralAttempts'] += NeutralAttempts

    # REFLECTION
    Run_Dict['Reflection'] = random_run_reflection_list[random.randint(0,len(random_run_reflection_list)-1)]

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

    # REFLECTION
    Activity_Dict['Reflection'] = random_activity_reflection_list[random.randint(0,len(random_activity_reflection_list)-1)]

    # ADD TO CSV
    act_testing_frame = pd.DataFrame(Activity_Dict)

    dummy_sections = Activity_Dict['Sections']
    dummy_tempos = Activity_Dict['Tempos']

    act_testing_frame['Sections'] = act_testing_frame['Sections'].astype('object')
    act_testing_frame['Tempos'] = act_testing_frame['Tempos'].astype('object')

    act_testing_frame.at[0, "Sections"] = dummy_sections
    act_testing_frame.at[0, "Tempos"] = dummy_tempos

    act_testing_frame[0:1].to_csv(user_csv, mode='a', index=False, header=False)

    print('\nWhat would you like to do next?')
    user_option = error_handling_int_plus(['Start a new piece', 'End session'],'Option> ')

    if user_option == 1:
        activity_start()
    elif user_option == 2:
        return 0

def error_handling_int_plus(message_list, message):
    variable_dummy = 0
    while variable_dummy != 1:
        for index, item in enumerate(message_list):
            print(f"[{index + 1}] {message_list[index]}")
        variable = input(message)
        print()
        try:
            if int(variable) in range(1, len(message_list) + 1):
                variable_dummy = 1
                variable = int(variable)
                break
            else:
                print(f"Please enter a number between 1 and {len(message_list)}\n")
        except ValueError:
            print('Please enter a valid number\n')

    return variable

session_start(False)
