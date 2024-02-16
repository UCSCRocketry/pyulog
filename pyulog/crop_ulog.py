
#! /usr/bin/env python

"""
Convert a ULog file into CSV file(s)
"""
#commandline usage: python <file.py> <file.ulg> -flight_start <insert timestamp value> -flight_end <insert timestamp value>
#OURS: python crop_ulog.py Jan_Subscale_Launch.ulg -flight_start 19:20 -flight_end 21:40
#make sure you use python not python3 this script does not support python3


from __future__ import print_function

import argparse
import numpy as np

from core import ULog
print("\nCompleted importing core file")

#pylint: disable=too-many-locals, invalid-name, consider-using-enumerate



def main():
    """Command line interface"""
    print("\nStarting argument parsing ...")

    parser = argparse.ArgumentParser(description='Crops ULog file')
    parser.add_argument('ulog_file', metavar='file.ulg', help='ULog input file')

    parser.add_argument(
        '-flight_start', '--flight_start', dest='flight_start',
        help="Start timestamp for flight data (in HH:MM)")

    parser.add_argument(
        '-flight_end', '--flight_end', dest='flight_end',
        help="End timestamp for flight data (in HH:MM)")

    args = parser.parse_args()
    print("Completed argument parsing")

    modify_ulog('../../Logs/Jan_Subscale_Launch.ulg')

<<<<<<< Updated upstream
 # Convert HH:MM format to seconds
    flight_start_seconds = convert_to_seconds(args.flight_start)
    flight_end_seconds = convert_to_seconds(args.flight_end)

    crop_ulog(args.ulog_file, flight_start_seconds, flight_end_seconds)

    print(" complete")

def convert_to_seconds(time_str):
    """Converts time in HH:MM format to seconds"""
    if time_str is None:
        return None

    hours, minutes = map(int, time_str.split(':'))
    return hours * 3600 + minutes * 60



def crop_ulog(ulog_file_name, flight_start, flight_end):
    """
    Crops the ULog file

    :param ulog_file_name: The ULog filename to open and read
    :param flight_start: Start time for conversion in seconds
    :param flight_end: End time for conversion in seconds

    :return: None
    """
    print("\nStarting to crop ...")
=======
def modify_ulog(ulog_file_name):
    print("\nStarting modification ...")
>>>>>>> Stashed changes

    ulog = ULog(ulog_file_name)
    data = ulog.data_list

    for d in data:
        # Determine the start index for the last 1000 data points
        start_index = max(0, len(d.data['timestamp']) - 1000)

        # Delete data points that are not in the last 1000 entries
        for key, value in d.data.items():
            d.data[key] = value[start_index:]

    # Save the modified data back to the original file
    ulog.write_ulog(ulog_file_name)
    print("\nModifications saved to the original file")

def crop_ulog(ulog_file_name):
    print("\nStarting to crop ...")

    ulog = ULog(ulog_file_name)
    ulog2 = ULog('copped.ulg')
    data = ulog.data_list

    for d in data:
        # Print basic information about the data message
        print(f"\nData message: {d.name}")
        print(f"Original timestamp length: {len(d.data['timestamp'])}")

        # Get the last 1000 data points
        last_index = len(d.data['timestamp'])
        start_index = max(0, last_index - 1000)  # Ensure start index is not negative

        # Crop the data and print lengths before and after cropping
        newData = {}
        for key, value in d.data.items():
            print(f"Length of '{key}' before cropping: {len(value)}")
            croppedData = value[start_index:last_index]
            newData[key] = croppedData
            print(f"Length of '{key}' after cropping: {len(newData[key])}")

        # Check if all fields have the same length
        lengths = [len(v) for v in newData.values()]
        if len(set(lengths)) != 1:
            print("Warning: Inconsistent data lengths after cropping")

        d.data = newData

    # Save cropped ulog file
    renamed_output_file = ulog_file_name[:-4] + '_last1000.ulg'
    ulog.write_ulog(renamed_output_file)
    print("\nCropped file saved")


if __name__ == "__main__":
    main()
