#!/usr/bin/python3
import numpy as np
import pandas as pd
import argparse
import datetime as dt


def CsvToDataframe(filename):
    ''' Reads csv to dataframe'''
    # Open file
    data = pd.read_csv(filename, sep=args.separator,
                       decimal=args.decimalpoint)
    # Cast to datetime
    data[data.columns[0]] = pd.to_datetime(
        data[data.columns[0]], format=args.dataformat)

    return data


def GetBeginEndTimestamps(data):
    '''
        First column treat as timestamp index.
        Returns begin, end
    '''
    return data[data.columns[0]][0], data[data.columns[0]][-1]


def SynchronizeDatetime(data, filename):
    ''' Synchronize datatime from file with given pands dataframe '''
    data2 = CsvToDataframe(filename)

    # Get begin end timestamps
    begin1, end1 = GetBeginEndTimestamps(data)
    begin2, end2 = GetBeginEndTimestamps(data2)

    # Select common range
    if (end1 < begin1) or (end2 < begin2):
        print('Error! No common range!')
    else:
        begin = max(begin1, begin2)
        end = min(end1, end2)

        data = data[data[data.columns[0]] >= begin]
        data = data[data[data.columns[0]] <= end]

    return data


# Arguments and config
# #####################################################
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str,
                    required=True, help='Input .csv file')
parser.add_argument('-d', '--decimalpoint', type=str, nargs='?', const='.',
                    required=False, help='Data CSV separator')
parser.add_argument('-s', '--separator', type=str, nargs='?', const=';',
                    required=False, help='Data CSV separator')
parser.add_argument('-df', '--dataformat', type=str, nargs='?', const='%Y-%m-%d %H:%M:%S,%f',
                    required=False, help='Data time format')
parser.add_argument('-x', '--synchronize-with-file', type=str,
                    required=False, help='Synchronize timestamps with file')
parser.add_argument('-r', '--removeEqualTo', type=float,
                    required=False, help='Remove all elements equal to.')
parser.add_argument('-rms', '--removems', action='store_true',
                    required=False, help='Remove miliseconds from all datetime fields.')
args = parser.parse_args()

if (args.separator is not None):
    separator = args.separator

# Open file
data = CsvToDataframe(args.input)

# Remove all equal to values from column 1
if (args.removeEqualTo is not None):
    data = data[data[data.columns[1]] != args.removeEqualTo]

# Synchronize datetime with other file
if (args.synchronize_with_file is not None):
    data = SynchronizeDatetime(data, args.synchronize_with_file)


print(data.values)

# Create .csv
print('Creation of .csv.')
