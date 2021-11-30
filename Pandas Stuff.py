# References: Udemy, Jose Portilla, Pierian Data Inc.

import time
from datetime import date
from datetime import datetime
import pandas as pd
import csv
'''
print(time.time())
print(date.today())
print(datetime.now())

pt_table = pd.read_csv("PT.csv")

pt_table.info()

print(pt_table[pt_table['Type'] == 'Activity1']['AttemptsTotal'])

# FIXME AND WE'RE OFF TO THE RACES BOYS!!!


print(datetime.now())
'''
mock_data = {
    'Date': 0,
    'Type': 0,
    'Time': 0,
    'Piece': [0],
    'Goals': ['Practice for a bit'],
    'Intent': [0],
    'Section': [0],
    'Tempo': [0],
    'AttemptsTotal': [0],
    'SuccessfulAttempts': [0],
    'UnsuccessfulAttempts': [0],
    'NeutralAttempts': [0],
    'Reflection': [0]
}

testing_frame = pd.DataFrame(mock_data)

print(testing_frame)

print()

testing_frame.to_csv('PT.csv', mode = 'a', index=False, header=True)

pt_table = pd.read_csv("PT.csv")

pt_table.info()

print(pt_table[pt_table['Type'] == 'Activity1']['AttemptsTotal'])

print(pt_table.iloc[1])
