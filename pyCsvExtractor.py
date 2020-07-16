#!/usr/bin/python3
import numpy as np
import pandas as pd
import argparse
import datetime

# defaults
separator = ';'


def signalsToCsv(filename, labels, signals):
    ''' Export all signals to single .csv'''
    filename = filename+'.csv'
    with open(filename, 'w+') as f:
        labels_row = separator.join(labels)
        f.write(labels_row)

        # Get max samples length
        maxLength = 0
        for i in range(len(signals)):
            maxLength = max(maxLength, len(signals[i]))

        # @TODO


def signalsToCsvs(filename, labels, signals, sampleRates):
    ''' Export all signals to multiple .csv'''
    for i in range(len(signals)):
        filepath = filename+labels[i]+'.csv'
        with open(filepath, 'w+') as f:
            # Labels
            f.write('Time[s]%c%s\n' % (separator, labels[i]))

            # Prepare time values
            if (args.timeAbsolute):
                time = startTime
                delta = datetime.timedelta(seconds=1.0/sampleRates[i])
            else:
                time = 0
                delta = 1.0/sampleRates[i]

            # Samples saving
            for sample in signals[i]:
                if (args.timeAbsolute):
                    # Absolute time used
                    text = '%s%c%2.2f\n' % (time.strftime(
                        '%Y-%m-%d %H:%M:%S.%f'), separator, sample)
                else:
                    # Relative time used
                    text = '%2.4f%c%2.2f\n' % (time, separator, sample)
                time += delta
                # Decimal mark conversion
                if (args.decimalpoint):
                    text = text.replace('.', ',')
                # Save
                f.write(text)


# Arguments and config
# #####################################################
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str,
                    required=True, help='Input .csv file')
parser.add_argument('-s', '--separator', type=str,
                    required=False, help='Data CSV separator')
parser.add_argument('-x', '--synchronize-with-file', type=str,
                    required=False, help='Synchronize timestamps with file')
parser.add_argument('-r', '--removeEqualTo', type=str,
                    required=False, help='Remove all elements equal to.')
parser.add_argument('-rms', '--removems', action='store_true',
                    required=False, help='Remove miliseconds from all datetime fields.')
parser.add_argument('-rt', '--removetime', action='store_true',
                    required=False, help='Remove time from all datetime fields.')
args = parser.parse_args()

if (args.separator is not None):
    separator = args.separator

# Open file
data = pd.read_csv(args.input)
print(data)

# Create .csv
print('Creation of .csv.')
signalsToCsvs(args.input, labels, signals, sampleRates)