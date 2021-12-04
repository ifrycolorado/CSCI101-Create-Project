import csv
import pandas as pd
import numpy as np
from numpy import *
import matplotlib.pyplot as plt

#  references: bar graph documentation https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html
#  references: constrained layout docs: https://matplotlib.org/stable/tutorials/intermediate/constrainedlayout_guide.html
#  references: plt.setp rotation https://stackoverflow.com/questions/31372953/plt-setp-alternative-for-subplots-or-how-to-set-text-rotation-on-x-axis-for-subp

data = pd.read_csv('Isaac.csv')
data.head()
dfp = pd.DataFrame(data)

def data_activity(user_profile):

    global dfp

    dfp = pd.read_csv(user_profile)
    user_type = input("What type would you like to retrieve? (Either Activity or Run)> ")
    type_frame = dfp['Type'] == user_type
    type_indices = list(dfp.index[type_frame])
    for index in type_indices:
        print(dfp.iloc[index])

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

def create_line(array_1,array_2,array_1_name,array_2_name):
    plt.plot(array_1, array_2, 'g')
    plt.xlabel(array_1_name)
    plt.ylabel(array_2_name)
    plt.title(f"{array_1_name} v. {array_2_name}")
    plt.show()

# FIXME all retrieve_[thing] function have similar syntax

def retrieve_dates():
    array_1 = np.array([])

    for item in set(dfp['Date']):
        array_1 = append(array_1,item)

    array_1.sort()

    return array_1

def retrieve_pieces():

    array_1 = np.array([])
    for item in set(dfp['Piece']):
        array_1 = append(array_1,item)

    array_1.sort()

    return array_1

def retrieve_time_by_date(array_1):

    array_2 = np.array([])

    for item in array_1:

        index_list_date = list(dfp.index[dfp['Date'] == item])
        index_list_activity = list(dfp.index[dfp['Type'] == 'Activity'])
        master_indices = []

        for index in index_list_date:
            if index in index_list_activity:
                master_indices.append(index)

        time_sum = 0
        for index in master_indices:
            # if dfp.iloc[index]['Type'] == 'Activity':
            minutes = seconds_to_minutes(float(dfp.iloc[index]['Time']))
            time_sum += minutes
        array_2 = append(array_2,time_sum)

    return array_2

def retrieve_time_by_piece(array_1):

    array_2 = np.array([])

    for item in array_1:

        index_list_date = list(dfp.index[dfp['Piece'] == item])
        index_list_activity = list(dfp.index[dfp['Type'] == 'Activity'])
        master_indices = []

        for index in index_list_date:
            if index in index_list_activity:
                master_indices.append(index)

        time_sum = 0
        for index in master_indices:
            # if dfp.iloc[index]['Type'] == 'Activity':
            minutes = seconds_to_minutes(float(dfp.iloc[index]['Time']))
            time_sum += minutes
        array_2 = append(array_2, time_sum)

    return array_2

def piece_retrieval(user_csv):

    print("Please select an activity or piece")

    previous_piece = []

    with open(user_csv, "r") as user_csv_file:
        user_csv_reader = csv.reader(user_csv_file)
        for line in user_csv_reader:
            print(line[3])
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
            print(f"\t\tReflections: {dfp.iloc[index]['Reflection']}")

# FIXME already in Activity and Run Input
def determine_last_session(user_profile):
    dfp = pd.read_csv(user_profile)
    last_index = int(dfp.size / 13) - 1
    last_session = int(dfp.iloc[last_index]['Session'])
    return last_session

# FIXME taken from matplotlib documentation
def create_bar_one_bar(array_1,array_2,array_1_name,array_2_name):

    width = 0.35
    x = np.arange(len(array_1))

    fig, ax = plt.subplots(constrained_layout = True)
    rects1 = ax.bar(x, array_2, width, label=array_1_name)

    ax.set_ylabel(array_2_name)
    ax.set_xlabel(array_1_name)
    ax.set_title(f"{array_1_name} by {array_2_name}")
    ax.set_xticks(x, array_1)

    ax.bar_label(rects1, padding=3)

    # Fixme why does this work?
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')

    plt.show()

def seconds_to_minutes(seconds):
    minutes = seconds // 60
    return minutes

'''
create_bar_one_bar(retrieve_dates(),retrieve_time_by_date(retrieve_dates()),"Date","Time")
create_line(retrieve_pieces(),retrieve_time_by_piece(retrieve_pieces()),"Piece","Time")

for index in index_list:
    if df.iloc[index]['Type'] == 'Activity':
        print(df)

with open("Isaac.csv", "r") as practice_file:
    section_array = np.array([])
    practice_reader = csv.reader(practice_file)
    for line in practice_reader:
        if line[1] == "Run":
            section_array = append(section_array, line[5])

with open("Isaac.csv", "r") as practice_file:
    tempo_list = []
    practice_reader = csv.reader(practice_file)
    for line in practice_reader:
        if line[1] == "Run":
            tempo_list.append(int(line[6]))
            
def retrieve_time_by_date(array_1):

    array_2 = np.array([])

    for item in array_1:

        index_list_date = list(dfp.index[dfp['Date'] == item])
        index_list_activity = list(dfp.index[dfp['Type'] == 'Activity'])
        master_indices = []

        for index in index_list_date:
            if index in index_list_activity:
                master_indices.append(index)

        time_sum = 0
        for index in master_indices:
            print(dfp.iloc[index])
            # if dfp.iloc[index]['Type'] == 'Activity':
            time_sum += float(dfp.iloc[index]['Time'])
        array_2 = append(array_2,time_sum)

    return array_2

def retrieve_time_by_piece(array_1):

    array_2 = np.array([])

    for item in array_1:

        index_list_date = list(dfp.index[dfp['Piece'] == item])
        index_list_activity = list(dfp.index[dfp['Type'] == 'Activity'])
        master_indices = []

        for index in index_list_date:
            if index in index_list_activity:
                master_indices.append(index)

        time_sum = 0
        for index in master_indices:
            # if dfp.iloc[index]['Type'] == 'Activity':
            print(dfp.iloc[index]['Time'])
            time_sum += float(dfp.iloc[index]['Time'])
        array_2 = append(array_2, time_sum)

    return array_2
'''

