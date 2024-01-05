#! /usr/bin/env python3
# coding=utf-8

import argparse
import csv
import datetime
import re
from collections import namedtuple
from os import listdir
from os.path import isfile, join

DATA_FIELDS = ["Bank_Name", "Transaction_Date", "Type", "Amount", "transaction_To", "transaction_From"]
Data = namedtuple('Data', DATA_FIELDS)


def main():
    data = []
    args = parse_args()
    for file in get_files(args.inDir, args.inPattern):
        data = read_data(data, file)
    if data:
       filepath = datetime.datetime.now().strftime("merged_" + "%Y-%m-%d-%H-%M.csv")
       write_data(data, DATA_FIELDS, filepath)
       print("Merged Successful")
    else:
       print("No Data Found. Please check Input file directory")


def parse_args():
    parser = argparse.ArgumentParser(description='Read-write data')
    parser.add_argument('-inDir', default='in', help='Directory containing files to process')
    parser.add_argument('-inPattern', default='', help='Regex to match file names in input directory')
    return parser.parse_args()


def read_data(data, file_path):
    f = lambda k, l: any(i for i in l if i in k)
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            amount = ''
            for k, v in row.items():
                if f(k, ["date", "time"]):
                    t_date = v
                if f(k, ["type", "transaction"]) or f(v, ["add", "remove"]):
                    t_type  = v
                if f(k, ['euro', 'cent', 'dollar']):
                    amount +=  v + " " + k + " "
                if 'amount' in k:
                    t_amount = str(v) + " rs"
                if k == 'to':
                    t_to = v
                if k == "from":
                    t_from = v
            if amount:
                t_amount = amount
            t_bank_name = file_path.split(".csv")[0]

            data.append(Data(t_bank_name, t_date, t_type, t_amount, t_to, t_from))
    return data


def write_data(data, header, file_path):
    with open(file_path, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=header, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for d in data:
            row_dict = {'Bank_Name': d.Bank_Name, 'Transaction_Date': d.Transaction_Date, 'Type': d.Type,
                        'Amount':d.Amount, 'transaction_To':d.transaction_To, 'transaction_From': d.transaction_From}
            writer.writerow(row_dict)


def get_files(dir_path, pattern):
    return [f for f in listdir(dir_path) if isfile(join(dir_path, f)) and f.endswith(pattern) and 'merged' not in f]


if __name__ == "__main__":
    main()
