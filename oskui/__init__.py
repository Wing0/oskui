'''
    Collection of custom-made UI functions for command line interface
'''
import os
import sys
import tty
import termios
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory


# Define getch function for cross-platform compatibility
def getch():
    """Get a single character from standard input without echoing to the screen."""
    try:
        # Win32
        import msvcrt
        return msvcrt.getch()
    except ImportError:
        # UNIX
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


# Define color codes for terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def ask_float_int(title, get_int=False):
    """
    Ask the user for a float or integer value.

    :param title: str, the prompt message
    :param get_int: bool, if True, only accept integer values
    :return: float|int|bool, the user's input or False if cancelled
    """
    print(title)
    user_value = None
    while user_value is None:
        user_input = input(
            'Type integer value, or q for cancel:' if get_int else 'Type float or integer value, or q for cancel:')
        if user_input.lower() == 'q':
            return False
        try:
            user_value = int(user_input) if get_int else float(user_input)
            if user_value > 0:
                break
        except ValueError:
            pass
        print('Incorrect value, please try again')
        user_value = None
    return user_value


def ask_file(message=None, key_press=True):
    """
    Prompt the user to select a file using a file dialog.

    :param message: str, optional message to display before opening the dialog
    :param key_press: bool, if True, wait for a key press before showing the dialog
    :return: str, path to the selected file
    """
    if message:
        print(message)
    if key_press:
        press_any_key('Select a file from your file system.')
    Tk().withdraw()
    return askopenfilename()


def ask_folder(message=None):
    """
    Prompt the user to select a folder using a directory dialog.

    :param message: str, optional message to display before opening the dialog
    :return: str, path to the selected folder
    """
    if message:
        print(message)
    press_any_key('Select a folder on your file system.')
    Tk().withdraw()
    return askdirectory()


def choice_menu(menu, title):
    """
    Display a menu of choices and prompt the user to make a selection.

    :param menu: list, the list of options to choose from
    :param title: str, the title of the menu
    :return: int|bool, the index of the chosen option or False if cancelled
    """
    print(title)
    for ind, option in enumerate(menu):
        print(f'{ind + 1}) {option}')
    print('q) Cancel')
    choice = input()
    while choice not in [str(i) for i in range(1, len(menu) + 1)] + ['q']:
        choice = input('Incorrect input. Try again:\n')
    return False if choice == 'q' else int(choice) - 1


def get_files(path, full_path=False, filter=None):
    """
    Get a list of files in a directory, optionally filtering by a substring.

    :param path: str, the directory path to search
    :param full_path: bool, if True, return the full path to the files
    :param filter: str, optional substring to filter the file names
    :return: list, the list of file names or paths
    """
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and (filter is None or filter in f)]
    return [os.path.join(path, f) for f in files] if full_path else files


def get_folders(path):
    """
    Get a list of folders in a directory.

    :param path: str, the directory path to search
    :return: list, the list of folder names
    """
    return [f for f in os.listdir(path) if not os.path.isfile(os.path.join(path, f))]


def toggle(choices, values, title):
    """
    Toggle between on and off values for a list of choices with pre-defined values.

    :param choices: list of str, the choice names
    :param values: list of int, the default choice values (0 or 1)
    :param title: str, instructions to the user
    :return: list of int, the updated choice values
    """
    valid = [str(i) for i in range(1, len(choices) + 1)]
    choice = None
    while choice is None or choice in valid:
        print(title)
        for ind, option in enumerate(choices):
            color = bcolors.OKGREEN if values[ind] else ''
            symbol = '+' if values[ind] else ' '
            print(f'{color}{ind + 1}) {symbol} {option}{bcolors.ENDC}')
        print('Any) Done')
        choice = input()
        if choice in valid:
            values[int(choice) - 1] = int(not values[int(choice) - 1])
    return values


def press_any_key(message=None):
    """
    Display a message and wait for the user to press any key.

    :param message: str, optional message to display
    :return: str, the key pressed by the user
    """
    if message:
        print(message)
    print('Press any key to continue...')
    return getch()


def prompt(message, default=None):
    """
    Prompt the user with a yes/no question.

    :param message: str, the message to display
    :param default: bool, the default value if the user presses Enter
    :return: bool, the user's response
    """
    alternatives = ['N', 'n', 'y', 'Y', '0', '1']
    info = '\n[Y/n]: ' if default else '\n[y/N]: ' if default is False else '\n[y/n]: '
    choice = input(message + info).strip()
    while choice not in alternatives + ['']:
        print('Incorrect input. Please try again.')
        choice = input(message + info).strip()
    return {'N': False, 'n': False, 'y': True, 'Y': True, '0': False, '1': True}.get(choice, default)


def warn(txt):
    """
    Print a warning message to the terminal.

    :param txt: str, the text of the warning message
    """
    print(f'{bcolors.WARNING}{txt}{bcolors.ENDC}')


def lower_case_name(title, unavailable=[]):
    """
    Prompt the user for a name that must be lowercase and not in the unavailable list.

    :param title: str, the prompt message
    :param unavailable: list of str, names that are not allowed
    :return: str, the chosen name
    """
    name = None
    while True:
        name = input(title).strip().lower()
        if len(name) >= 3 and name not in unavailable and name.islower():
            break
        elif len(name) < 3:
            print('Name too short (minimum 3 characters). Try again:')
        elif name in unavailable:
            print('The name is taken or not available. Please give a different name:')
        else:
            print('Invalid name. All characters need to be lower case letters. Try again:')
    return name