from datetime import datetime

def scuffed_split(s):
    if '","' in s:
        g = s.split('","')
        return [k.strip('"') for k in g]
    return s.split(',')


class DateChecker:
    def __init__(self, format, dateIx=0):
        self.format = format
        self.dateIx = dateIx
        self.nameIx = 1 if dateIx == 0 else 0

    def check_date_format(self, obj):
        g = scuffed_split(obj)
        if self.dateIx >= len(g):
            return False
        date_str = g[self.dateIx]
        try:
            datetime.strptime(date_str, self.format)
            return True
        except ValueError:
            return False
    
    def convert(self, obj):
        g = scuffed_split(obj)
        date_str = g[self.dateIx]
        date = datetime.strptime(date_str, self.format)
        return g[self.nameIx], date.timestamp()

# Usage
checkers = [
    DateChecker("%m/%d/%Y", 0),
    DateChecker("%m/%d/%Y %I:%M:%S %p", 1),
    DateChecker("%Y-%m-%d %H:%M:%S", 2)
]
def get_checker(obj):
    for checker in checkers:
        if checker.check_date_format(obj):
            return checker
    # assert False, f"no checker for {obj}"
    return None


# tests = [
#     '01/07/2022,Am11 Dm7 Em7 Am - Stale Window.m4a',
#     '206263000.wav,12/25/2023 12:18:36 PM',
#     'dead pitchy.mp3,1593737201.0,2020-07-02 20:46:41',
#     '"your facade, day in and day out 75.wav","6/2/2021 1:24:21 AM"'
# ]
# for test in tests:
#     result = get_checker(test).check_date_format(test)
#     print(result)  # Output: True

#     result = get_checker(test).convert(test)
#     print(result)  # Output: True