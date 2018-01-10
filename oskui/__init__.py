'''
    Collection of custom-made UI functions for command line interface
'''
from os import listdir
from os.path import isfile, join
from Tkinter import Tk
from tkFileDialog import askopenfilename, askdirectory
try:
    # Win32
    from msvcrt import getch as getch_win

    def getch():
        return getch_win()
except ImportError:
    # UNIX
    def getch():
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


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
    print title
    user_value = None
    if get_int:
        print 'Type integer value, or q for cancel:'
    else:
        print 'Type float or integer value, or q for cancel:'
    while user_value is None:
        user_value = raw_input()
        if user_value == 'q':
            return False
        elif get_int:
            try:
                user_value = int(user_value)
                if int(user_value) > 0:
                    break
            except ValueError:
                pass
        else:
            try:
                user_value = float(user_value)
                if float(user_value) > 0:
                    break
            except ValueError:
                pass
        print 'Incorrect value, plese try again'
        user_value = None

    return user_value


def ask_file(message=None, key_press=True):
    '''
    Displays message if given and let's the user to select a file
    in the file system
    @params:
    - message: string, message displayed to the user
    @output:
    - path: string, path to the selected file
    '''
    if message is not None:
        print message
    if key_press:
        press_any_key('Select a file from your file system.')
    Tk().withdraw()
    path = askopenfilename()
    return path


def ask_folder(message=None):
    '''
    Displays message if given and let's the user to select a folder
    on the file system
    @params:
    - message: string, message displayed to the user
    @output:
    - path: string, path to the selected folder
    '''
    if message is not None:
        print message
    press_any_key('Select a folder on your file system.')
    Tk().withdraw()
    path = askdirectory()
    return path


def choice_menu(menu, title):
    print title
    choice = None
    for ind, option in enumerate(menu):
        print '%s) %s' % (ind + 1, option)
    print 'q) Cancel'
    while choice is None or (
        choice not in [str(i) for i in range(1, len(menu) + 1)] + ['q']
    ):
        if choice is not None:
            choice = raw_input('Incorrect input. Try again:\n')
        else:
            choice = raw_input()

    if choice == 'q':
        return False
    else:
        return int(choice) - 1


def get_files(path, full_path=False, filter=None):
    files = [
        f for f in listdir(path)
        if isfile(join(path, f)) and (filter is None or filter in f)]
    if full_path:
        files = ["%s/%s" % (path, f) for f in files]
    return files


def get_folders(path):
    return [f for f in listdir(path) if not isfile(join(path, f))]


def toggle(choices, values, title):
    '''
    Enables user to toggle between on and off values matching a list of options
    with pre-defined values. Toggle is based on a color and symbol.

    @params:
    - choices: list of strings, list of choice names
    - values: list of integers, list of default choice values, 0 or 1
    - title: string, instructions to the user

    @output:
    - values: list of integers, list of returned choice values
    '''

    valid = [str(i) for i in range(1, len(choices) + 1)]
    choice = None
    while choice is None or choice in valid:
        print title
        for ind, option in enumerate(choices):
            if values[ind]:
                print (
                    bcolors.OKGREEN +
                    '%s) %s %s' % (ind + 1, '+', option) +
                    bcolors.ENDC)
            else:
                print '%s) %s %s' % (ind + 1, ' ', option)
        print 'Any) Done'
        choice = raw_input()

        if choice in valid:
            values[int(choice) - 1] = int(not values[int(choice) - 1])

    return values


def press_any_key(message=None):
    '''
    Displays message if given and waits for user input
    @params:
    - message: string, message displayed to the user
    @output:
    - key: string, key pressed by the user
    '''
    if message is not None:
        print message
    print 'Press any key to continue...'
    return getch()


def prompt(message, default=None):
    choice = None
    alternatives = ['N', 'n', 'y', 'Y', '0', '1']
    if default is False:
        info = '\n[y/N]: '
    elif default is True:
        info = '\n[Y/n]: '
    else:
        info = '\n[y/n]: '

    if default is not None:
        alternatives.append('')
    while choice is None or choice not in alternatives:
        if choice is not None:
            print 'Incorrect input. Please try again.'
        choice = raw_input(message + info)
    if choice in ['N', 'n', '0']:
        return False
    elif choice in ['Y', 'y', '1']:
        return True
    else:
        return default


def warn(txt):
    print (
        bcolors.WARNING +
        txt +
        bcolors.ENDC)


def lower_case_name(title, unavailable=[]):
    name = None
    while name is None or (
            sum([0 if c.islower() else 1 for c in name]) != 0) or (
            len(name) < 3) or name in unavailable:
        if name is None:
            name = raw_input(title)
        elif len(name) < 3:
            name = raw_input(
                'Name too short (minimum 3 characters). Try again:\n')
        elif name in unavailable:
            name = raw_input((
                'The name is taken or not available.'
                ' Please give a different name:\n'))
        else:
            name = raw_input((
                'Invalid name. All characters need to be lower case letters. '
                'Try again:\n'))
    return name
