#!/usr/bin/python3
import numpy as np
import pandas as pd
import argparse
import datetime as dt

# List of all separators
separators = [ ',', ';', '.', '#', ':', '\t' ]

# List of possible datetime timestamp formats
timestamp_formats = [
'%Y-%m-%d %H:%M:%S,%f',
'%Y-%m-%d %H:%M:%S',
'%Y-%m-%d %H:%M',
'%Y-%m-%d',
'%H:%M',
]

def StrDateToDatetime(string):
    ''' Creates datetime from string formatted date.'''
    date = None
    for format in timestamp_formats:
        try:
            date = dt.datetime.strptime(string,format)
        except:
            ''' Do nothing '''
        if (date is not None):
            break

    return date


def CsvToDataframe(filename, format):
    ''' Reads csv to dataframe'''
    # Open file
    data = pd.read_csv(filename, sep=args.separator, decimal=args.decimalpoint)

    # Firs column is treat as index/timestamp.
    # If first column is string then try to convert it to datetime
    if type(data[data.columns[0]][0]) == str:
        # Change to dt date timestamp
        for index in range(len(data[data.columns[0]])):
            text = data[data.columns[0]][index]
            data[data.columns[0]].values[index] = dt.datetime.strptime(
                text, format)
    
    # Add base datetime to first column
    if (args.date_base is not None):
        print ("Base date given %s." % (args.date_base))
        base = StrDateToDatetime(args.date_base)

        # Change to dt date timestamp
        column = []
        for index in range(len(data[data.columns[0]])):
            column.append(base + dt.timedelta(seconds=data[data.columns[0]][index]))

        data[data.columns[0]] = column

    return data

def DataframeToCsv(data):
    ''' Dataframe to csv save'''
    separator = args.separator
    
    # If separator longer than 1 character, trim it
    if (type(separator) == str):
        separator = separator[0]
        
    # If separator == decimalpoint then choose other
    i = 0
    while (separator == args.decimalpoint):
        separator = separators[i]
        i += 1
        
    print('Creation of .csv.')
    data.to_csv('Changed.'+args.input, index=False,
                sep=separator, decimal=args.decimalpoint)


def GetBeginEndTimestamps(data):
    '''
        First column treat as timestamp index.
        Returns begin, end
    '''
    return data[data.columns[0]].iloc[0], data[data.columns[0]].iloc[-1]


def SynchronizeDatetime(data, filename):
    ''' Synchronize datatime from file with given pands dataframe '''
    data2 = CsvToDataframe(filename, args.dateformat2)

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
        print('Selected data from range', begin, 'to', end)

    return data


def FilterGrossErrors(window):
    ''' Filter gross errors from data window'''
    average = sum(window) / len(window)
    sample = window[-1]
    diffrence = abs(average-sample)
    # If more than 100% diffrence
    if (diffrence > average):
        print('Filtered %2.2f' % sample)
        return average
    return sample

def PrintInfo(data):
    ''' Prints info about dataframe '''
    print('Data rows %u.' % len(data))
    print('Data columns %u.' % len(data.columns))
    for i,column in enumerate(data.columns):
        print("Column %u '%s'." % (i,column))
        print(type(data[data.columns[i]][0]))
        #@ TODO Variance
        #@ TODO Max
        #@ TODO Min
        #@ TODO Mean
        #@ TODO Median
        


# Arguments and config
# #####################################################
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str,
                    required=True, help='Input .csv file')
parser.add_argument('-d', '--decimalpoint', type=str, nargs='?', const='.',
                    required=False, help='Data CSV separator')
parser.add_argument('-s', '--separator', type=str, nargs='?', const=';',
                    required=False, help='Data CSV separator')
parser.add_argument('-db', '--date-base', type=str,
                    required=False, help='Start basedate of csv')
parser.add_argument('-df', '--dateformat', type=str, nargs='?', const='%Y-%m-%d %H:%M:%S,%f', default='%Y-%m-%d %H:%M:%S,%f',
                    required=False, help='Data time format')
parser.add_argument('-df2', '--dateformat2', type=str, nargs='?', const='%Y-%m-%d %H:%M:%S,%f', default='%Y-%m-%d %H:%M:%S',
                    required=False, help='Data time format')
parser.add_argument('-dd', '--dropduplicates', action='store_true',
                    required=False, help='Drops duplicates.')
parser.add_argument('-f', '--filterErrors', type=int,
                    required=False, help='Filter gross errors window size.')
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
data = CsvToDataframe(args.input, args.dateformat)

PrintInfo(data)

# Remove miliseconds
if (args.removems is True):
    for index in range(len(data[data.columns[0]])):
        element = data[data.columns[0]][index]
        data[data.columns[0]].values[index] = element.replace(microsecond=0)

if (args.dropduplicates is True):
    length = len(data)
    data.drop_duplicates(data.columns[0], inplace=True)
    newLength = len(data)
    print('Dropped %u rows.' % (length-newLength))

# Remove all equal to values from column 1
if (args.removeEqualTo is not None):
    length = len(data)
    data = data[data[data.columns[1]] != args.removeEqualTo]
    newLength = len(data)
    print('Dropped %u rows.' % (length-newLength))

# Filter gross errors
if (args.filterErrors is not None):
    data = data[[data.columns[1]]].rolling(
        args.filterErrors).apply(FilterGrossErrors)

# Synchronize datetime with other file
if (args.synchronize_with_file is not None):
    data = SynchronizeDatetime(data, args.synchronize_with_file)
    
# Preview of data TODO

# Save data
DataframeToCsv(data)
