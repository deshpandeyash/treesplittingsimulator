import os
from datetime import  date
import sys


def make_result_folder():
    today = date.today()
    today_string = today.strftime("%b-%d-%Y")
    date_time_folder = 'Results/' + today_string + "Tests/"
    if not os.path.exists(date_time_folder):
        os.makedirs(date_time_folder)
    return date_time_folder


def make_result_txt(date_time_folder):
    orig_stdout = sys.stdout
    txt_file = open(date_time_folder + 'Output.txt', 'w+')
    sys.stdout = txt_file
    return txt_file, orig_stdout


def close_txt_file(txt_context):
    txt_file = txt_context[0]
    orig_stdout = txt_context[1]
    sys.stdout = orig_stdout
    txt_file.close()


def still_print(date_time_folder):
    txt_file = open(date_time_folder + 'Output.txt', 'r')
    contents = txt_file.read()
    print(contents)