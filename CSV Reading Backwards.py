import csv

with open("Isaac.csv",'r') as test_file:
    test_reader = csv.reader(test_file)
    for i in reversed(test_reader):
        print(i)
        break

