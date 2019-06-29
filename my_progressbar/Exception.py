class NegativeRange(Exception):
    def __init__(self):
        pass


class ValueOutOfRange(Exception):
    def __init__(self, value):
        self._value = value

    def get_value(self):
        return self._value

class StartNotCalled(Exception):
    def __init__(self):
        pass