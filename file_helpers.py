import os
import shutil
from datetime import date, time
import tikzplotlib
from matplotlib import pyplot as plt


def create_today_folder(trial_no):
    """
    Creates the Today Folder with a given trial number. IF the folder already exists, then the next available one
    with the trial number is chosen
    :param trial_no: the trial number in the today folder
    :return: the today folder string
    """
    today = date.today()
    today_string = today.strftime("%b-%d-%Y")
    today_folder = 'Results/DailyResults/' + today_string + "/Trial" + str(trial_no) + "/"
    while os.path.exists(today_folder):
        trial_no += 1
        today_folder = 'Results/DailyResults/' + today_string + "/Trial" + str(trial_no) + "/"
    create_folder(today_folder)
    return today_folder


def get_time():
    """
    Dummy function to reduce the number of imports everywhere
    :return: time from datetime
    """
    return time


def create_folder(folder_path):
    """
    Checks if the path exists already and creates a directory if it doesnt. If it exists then does nothing
    :param folder_path: the path to which to create folder
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def delete_files(file_list):
    """
    We need to delete a bulk number of files at a time. Then we can use this.
    :param file_list: The list of paths of the files to be deleted
    """
    for f in file_list:
        fname = f.rstrip()  # or depending on situation: f.rstrip('\n')
        # or, if you get rid of os.chdir(path) above,
        # fname = os.path.join(path, f.rstrip())
        if os.path.isfile(fname):  # this makes the code more robust
            os.remove(fname)


def delete_dir(the_directory):
    """
    Removes the directory
    :param the_directory: the path of the directory to be removed
    """
    shutil.rmtree(the_directory)


def save_and_close_fig(fig_name):
    """
    Take a figure and saves it in TIKZ and PNG in the folder path supplied
    :param fig_name: the path to which the figure must be saved
    """

    plt.savefig(fig_name + '.png', dpi=300)
    tikzplotlib.save(fig_name, encoding="UTF-8")
    plt.close()
