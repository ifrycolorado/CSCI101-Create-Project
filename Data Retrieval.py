import csv
import pandas as pd
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from datetime import date
import random

# references: bar graph documentation https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html
# references: constrained layout docs: https://matplotlib.org/stable/tutorials/intermediate/constrainedlayout_guide.html
# references: plt.setp rotation https://stackoverflow.com/questions/31372953/plt-setp-alternative-for-subplots-or-how-to-set-text-rotation-on-x-axis-for-subp
# references: date checking from Python Docs https://docs.python.org/3/library/datetime.html
# references: making dictionaries subscriptable https://www.kite.com/python/answers/how-to-index-a-dictionary-in-python

Notes_Dict = {'quarter':'♩','eigth':'♪','eighth_beamed':"♫",'sixteenth_beamed':'♬','repeat_left':'𝄆','repeat_right':'𝄇'}

data = pd.read_csv('Isaac.csv')
data.head()
dfp = pd.DataFrame(data)

user_csv = 'Isaac.csv'

user_heading_list = ['Date', 'Action Type', 'Time (in seconds)', 'Piece', 'Goals', 'Sections', 'Tempos', 'Total Attempts',
                      'Successful Attempts', 'Unsuccessful Attempts', 'Unfocused Attempts',
                      'Reflection', 'Session Identifier']

# pulling
def determine_last_session(user_profile):
    pt_table = pd.read_csv(user_profile)
    last_index = int(pt_table.size / 13) - 1
    last_session = int(pt_table.iloc[last_index]['Session'])
    return last_session

def piece_retrieval_data(user_csv):

    print("Please select an activity or piece")

    previous_piece = []

    with open(user_csv, "r") as user_csv_file:
        user_csv_reader = csv.reader(user_csv_file)
        for line in user_csv_reader:
            if line[1] == "Activity":
                if line[3] not in previous_piece:
                    previous_piece.append(line[3])

    for index, piece in enumerate(previous_piece):
        print(f"[{index}] {piece}")

    try:
        piece_selection = int(input("Selection> "))
    except (TypeError, ValueError, IndexError):
        print("Please enter a valid number")

    # FIXME Error Handling
    user_piece = previous_piece[piece_selection]

    return user_piece

def pull_reflection_by_piece(user_profile):
    selection = piece_retrieval_data(user_profile)
    for index in list(dfp.index[dfp['Piece'] == selection]):
        print(f"Reflection on {dfp.iloc[index]['Date']} in {dfp.iloc[index]['Type']}: {dfp.iloc[index]['Reflection']}")

def retrieve_item(retrieving):

    array_1 = np.array([])

    for item in set(dfp[retrieving]):
        array_1 = append(array_1,item)

    array_1.sort()

    return array_1

def retrieve_thing_by_structure(array_1,structure,thing):

    array_2 = np.array([])

    for item in array_1:

        index_list_date = list(dfp.index[dfp[structure] == item])
        index_list_activity = list(dfp.index[dfp['Type'] == 'Activity'])
        master_indices = []

        for index in index_list_date:
            if index in index_list_activity:
                master_indices.append(index)

        time_sum = 0
        for index in master_indices:
            minutes = seconds_to_minutes(float(dfp.iloc[index][thing]))
            time_sum += minutes
        array_2 = append(array_2, time_sum)

    return array_2

def retrieve_thing_by_structure_not_time(array_1,structure,thing):

    array_2 = np.array([])

    for item in array_1:

        index_list_date = list(dfp.index[dfp[structure] == item])
        index_list_activity = list(dfp.index[dfp['Type'] == 'Activity'])
        master_indices = []

        for index in index_list_date:
            if index in index_list_activity:
                master_indices.append(index)

        time_sum = 0
        for index in master_indices:
            minutes = float(dfp.iloc[index][thing])
            time_sum += minutes
        array_2 = append(array_2, time_sum)

    return array_2

def piece_retrieval(user_csv,activity_define=True):

    print("Please select an activity or piece:\n")

    previous_piece = []

    with open(user_csv, "r") as user_csv_file:
        user_csv_reader = csv.reader(user_csv_file)
        for line in user_csv_reader:
            if line[1] == "Activity":
                if line[3] not in previous_piece:
                    previous_piece.append(line[3])

    for index,piece in enumerate(previous_piece):
        print(f"[{index}] {piece}")

    if activity_define:
        print(f"[{len(previous_piece)}] Define a new activity")

    # error handling
    dummy = 0
    while dummy != 1:
        try:
            piece_selection = int(input("Selection> "))
            if piece_selection == len(previous_piece):
                user_piece = input("Activity name")
            else:
                user_piece = previous_piece[piece_selection]
            print()
            dummy = 1
        except (TypeError, ValueError, IndexError):
            print("\nERROR: Please enter a valid number\n")

    #FIXME Error Handling

    return user_piece

# FIXME already in Activity and Run Input
def generate_report_last_session(user_csv):

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
            print(f"Piece: {dfp.iloc[index]['Piece']}")
            print(f"Overall reflection: {dfp.iloc[index]['Reflection']}")

    for counter,index in enumerate(run_indices):
        if dfp.iloc[index]["Type"] == 'Run':
            print(f"\tAction type: {dfp.iloc[index]['Type']}_{counter}")
            print(f"\t\tTempos: {dfp.iloc[index]['Tempos']}")
            print(f"\t\tSections: {dfp.iloc[index]['Sections']}")
            print(f"\t\tReflections: {dfp.iloc[index]['Reflection']}\n")

# FIXME already in Activity and Run Input
def determine_last_session(user_profile):
    dfp = pd.read_csv(user_profile)
    last_index = int(dfp.size / 13) - 1
    last_session = int(dfp.iloc[last_index]['Session'])
    return last_session

# FIXME taken from matplotlib documentation
def create_bar_one_bar(array_x,array_y,array_x_name,array_y_name):

    width = 0.35
    x = np.arange(len(array_x))

    # create object
    fig, ax = plt.subplots(constrained_layout = True)
    rects1 = ax.bar(x, array_y, width, label=array_x_name)

    # set axis names and labels
    ax.set_ylabel(array_y_name)
    ax.set_xlabel(array_x_name)
    ax.set_title(f"{array_x_name} by {array_y_name}")
    ax.set_xticks(x, array_x)

    ax.bar_label(rects1, padding=3)

    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')

    plt.show()

def create_three_bar(array_beta,array_x1,array_x2,array_x3,array_y,array_x1_name,array_x2_name,array_x3_name,array_y_name):

    x = np.arange(len(array_x1))  # Locations of labels along x axis
    width = 0.15  # the width of the bars

    fig, ax = plt.subplots(constrained_layout = True)
    rects1 = ax.bar(x, array_x1, width, label=array_x1_name)
    rects2 = ax.bar(x + width, array_x2, width, label=array_x2_name)
    rects3 = ax.bar(x + width * 2, array_x3, width, label=array_x3_name)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(array_y_name)
    ax.set_title(f"Attempts by {array_y_name}")
    ax.set_xticks(x, array_beta)
    ax.legend()

    ax.bar_label(rects1, padding=2)
    ax.bar_label(rects2, padding=2)
    ax.bar_label(rects3, padding=2)

    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')

    plt.show()

# generating report
def generate_report_by_parameter(start_input = "0000-00-00",end_input = '9999-99-99',piece=''):
    index_list_date_start = 0
    index_list_date_end = len(dfp)
    piece_list = list(dfp.head(n=0))
    top_heads = list(dfp.head(n=0))

    if start_input != '0000-00-00':
        start_date = validity_of_date(start_date=start_input,start=True)
        index_list_date_start = list(dfp.index[dfp['Date'] == start_date])[0]
    if end_input != '9999-99-99':
        end_date = validity_of_date(end_date=end_input, end=True)
        index_list_date_end = list(dfp.index[dfp['Date'] == end_date])[-1]
    if piece != '':
        piece_list = list(dfp.index[dfp['Piece'] == piece])[1:]
    elif piece == '':
        piece_list = list(range(len(dfp)))

    master_indices = []

    for index in list(range(index_list_date_start,index_list_date_end+1)):
        for heading_index in piece_list:
            if heading_index == index:
                master_indices.append(heading_index)

    for index in master_indices:
        for index_lowest in range(len(user_heading_list)):
            if index_lowest == 0:
                print(f"{user_heading_list[index_lowest]}: {dfp.iloc[index][top_heads[index_lowest]]}")
            else:
                print(f"\t{user_heading_list[index_lowest]}: {dfp.iloc[index][top_heads[index_lowest]]}")
        print()

# BACKGROUND CALLS
def validity_of_date(start_date='',end_date='',start=False,end=False):
    if start:
        actual_start = dfp.iloc[0]['Date']
        if start_date <= actual_start:
            return actual_start
        elif start_date > actual_start:
            return start_date
    if end:
        actual_end = dfp.iloc[-1]['Date']
        if end_date >= actual_end:
            return actual_end
        elif end_date < actual_end:
            return end_date

def get_desired_date(message):
    dummy = 0
    print(message)
    print("(Please enter the date in a YYYY-MM-DD format)")
    while dummy != 1:
        user_date = input("Date> ")
        try:
            returning = str(date.fromisoformat(user_date))
            dummy = 1
            break
        except ValueError:
            print("Please enter a valid date\n")
    return returning

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

def random_note_pick():
    notes_list = list(Notes_Dict)
    my_number = random.randint(0,3)
    return notes_list[my_number]

# MENUS
def data_main_menu():
    #print(f"Welcome, {user_profile}, to the Data Menu")
    user_input = error_handling_int_plus(['View Graphs', 'Generate Summaries','Return to Main Menu'], "Option> ")
    if user_input == 1:
        print(f"{Notes_Dict[random_note_pick()]} Welcome to the Graphing Menu!\n")
        graph_menu()
    elif user_input == 2:
        print(f"{Notes_Dict[random_note_pick()]} Welcome to the Summary Menu!\n")
        summary_menu()
    elif user_input == 3:
        return 0
        #main_menu_valid(False)

def summary_menu():
    user_input = error_handling_int_plus(['Generate Summary by Date and/or Piece','Generate Summary of Last Session',
                                          'Return to Data Main Menu'],'\nOption> ')
    if user_input == 1:
        summary_by_parameter()
    elif user_input == 2:
        generate_report_last_session(user_csv)
        summary_menu()
    elif user_input == 3:
        data_main_menu()

def summary_by_parameter():

    print('Would you like to filter by date?')
    date_choice = error_handling_int_plus(['Yes','No'], 'Option> ')
    if date_choice == 1:
        starting_date = get_desired_date('\nEnter the earliest date you want:')
        ending_date = get_desired_date('\nEnter the latest date you want:')
    else:
        starting_date = '0000-00-01'
        ending_date = '9999-99-98'

    print('Would you like to filter by piece?')
    piece_choice = error_handling_int_plus(['Yes','No'], 'Option> ')
    if piece_choice == 1:
        piece_filter = piece_retrieval(user_csv,activity_define=False)
    else:
        piece_filter = ""

    generate_report_by_parameter(starting_date,ending_date,piece_filter)

    summary_menu()


def graph_menu():
    user_choice = error_handling_int_plus(['View Graph of Time per Date/Piece','View Graphs of Attempts','Return to Data Main Menu'],'Option> ')
    if user_choice == 1:
        graph_one_bar_menu()
    elif user_choice == 2:
        graph_three_bar_menu()

def graph_one_bar_menu():
    user_choice = error_handling_int_plus(['Analyze by Pieces','Analyze by Date'],'Option> ')
    if user_choice == 1:
        create_bar_one_bar(retrieve_item('Piece'),retrieve_thing_by_structure(retrieve_item('Piece'),'Piece','Time'),'Piece','Time')
    if user_choice == 2:
        create_bar_one_bar(retrieve_item('Date'),retrieve_thing_by_structure(retrieve_item('Date'),'Date','Time'),'Date','Time')

    graph_menu()

def graph_three_bar_menu():
    user_choice = error_handling_int_plus(['Analyze by Pieces', 'Analyze by Date'], 'Option> ')
    if user_choice == 1:
        create_three_bar(
            retrieve_item('Piece'),
            retrieve_thing_by_structure_not_time(retrieve_item("Piece"), 'Piece', 'SuccessfulAttempts'),
            retrieve_thing_by_structure_not_time(retrieve_item('Piece'), 'Piece', 'UnsuccessfulAttempts'),
            retrieve_thing_by_structure_not_time(retrieve_item('Piece'), 'Piece', 'NeutralAttempts'),
            retrieve_thing_by_structure_not_time(retrieve_item('Piece'), 'Piece', 'AttemptsTotal'),
            'Successful', 'Unsuccessful', 'Unfocused', 'Piece')
    if user_choice == 2:
        create_three_bar(
            retrieve_item('Date'),
            retrieve_thing_by_structure_not_time(retrieve_item("Date"), 'Date', 'SuccessfulAttempts'),
            retrieve_thing_by_structure_not_time(retrieve_item('Date'), 'Date', 'UnsuccessfulAttempts'),
            retrieve_thing_by_structure_not_time(retrieve_item('Date'), 'Date', 'NeutralAttempts'),
            retrieve_thing_by_structure_not_time(retrieve_item('Date'), 'Date', 'AttemptsTotal'),
            'Successful', 'Unsuccessful', 'Unfocused', 'Date')
    graph_menu()

data_main_menu()