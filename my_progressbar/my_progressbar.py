import time

from colorama import Fore
from my_progressbar.Exception import *


class ProgressBar:
    # max_val = max limit
    # min_val = min limits
    # current_value = value currently in progressbar
    # name = name printed before the progress bar
    # opening = char that open the bar
    # progress_indicator = char that show progress
    # spacer = char that is between progress and closing
    # closing = char that close the bar
    # jump_length = default value that is add to value
    # bar_length = number of char that is between opening and close

    def __init__(self, max_val: int, name: str, current_value: int = None,
                 jump_length: int = 1, min_val: int = 0, opening: str = '[',
                 closing: str = ']', progress_indicator: str = '=',
                 spacer: str = ' ', bar_length: int = 80):

        self._last_update_time = None

        self._max_val = max_val
        self._min_val = min_val
        self._range = self._max_val - self._min_val
        self._current_value = current_value if current_value is not None else min_val

        self._name = name
        self._opening_string = opening
        self._progress_indicator = progress_indicator
        self._spacer = spacer
        self._closing_string = closing

        self._jump_length = jump_length
        self._bar_length = bar_length

        if self._range <= 0:
            raise NegativeRange
        self._percentage = self.calculate_percentage(self._current_value)

    def calculate_percentage(self, value):
        if value > self._max_val or value < self._min_val:
            raise ValueOutOfRange(value)

        # return percentage base on min and max
        return int(abs((value-self._min_val)/self._range) * 100)

    def start(self):
        # must be called if you want to use this progressbar
        self._last_update_time = time.time()
        self.update(self._current_value)

    def get_percentage(self):
        return self._percentage

    def update(self, new_value: int = None):
        # update progress bar to the value
        # return time from last update

        if new_value is None:
            new_value = self._current_value + self._jump_length

        if self._last_update_time is None:
            raise StartNotCalled

        time_diff = time.time() - self._last_update_time
        self._last_update_time = time.time()  # update

        self._percentage = self.calculate_percentage(new_value)
        self._current_value = new_value
        self.print()
        return time_diff

    def print(self):
        if self._percentage == 100:
            # print finish in green when counter arrive to 100
            print('\r' + self._name, Fore.LIGHTGREEN_EX + 'Finished', end=Fore.RESET)

        else:
            # print finish in green when counter arrive to 100
            n_indicator = int(((self._percentage / 100) * self._bar_length)/len(self._progress_indicator))
            n_spacer = int((self._bar_length - n_indicator)/len(self._spacer))

            print('\r' + self._name, end=' ')
            print(self._current_value, '/', self._max_val, sep='', end='')
            print(self._opening_string, self._progress_indicator * n_indicator,
                  self._spacer * n_spacer, self._closing_string, sep='', end=' ')
            print(self._percentage, '%', sep='', end='', flush=True)

    def finish(self):
        # make sure that progress is to 100 and make sure that you cant overwrite the bar whit update
        self.update(self._max_val)
        self._last_update_time = None
        print()

    def reset(self):
        self.update(self._min_val)
