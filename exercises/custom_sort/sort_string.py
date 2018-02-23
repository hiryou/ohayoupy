import re as RE
from datetime import datetime as DATETIME

"""
# 3 types of elements, priority order of matching is:
# type=1. Date: yyyy-mm-dd, yyyy/mm/dd
# type=2. Number: 2.5, -3, etc
# type=3. Alphabet

Algorithm: for a given string s, we use a complex REGEX to match sequence of different types (date, number, alphabet)
in s from left->right. Therefore, a string s has a sequence of types. Now to compare 2 strings s1, s2:
* if their type sequences are different, compare the type sequence. This simple technique allow all strings with 
    same/similar-prefix type sequence to be grouped together
* else, iterate through the type sequence of both strings and compare them pair-wise
* Example: 
    s1 = "Valentine 2017/02/14 200" -> type_sequence = "3-1-2"
    s2 = "2017/03/14 is Valentine" -> type_sequence = "1-3-3"
    s3 = "Ended 2017/02/15 300" -> type_sequence = "3-1-2" 
    => sorted = [s2, s3, s1]
"""


class Element:
    type = 0  # 1 = date, 2 = number, 3 = alphabet
    value = None  # for date: date, number: number, alphabet: string

    def __init__(self, type, value):
        self.type = type
        self.value = value

    @staticmethod
    def as_date(str):
        for fmt in ('%Y/%m/%d', '%Y-%m-%d'):
            try:
                dt = DATETIME.strptime(str, fmt)
                return Element(1, dt)
            except ValueError:
                pass
        raise ValueError('invalid datetime: ' + str)

    @staticmethod
    def as_number(str):
        return Element(2, float(str))

    @staticmethod
    def as_string(str):
        return Element(3, str)

    @classmethod
    def compare_string(cls, a, b):
        va = a.lower()
        vb = b.lower()
        if va == vb:
            return 0
        elif va < vb:
            return -1
        return +1

    @classmethod
    def compare(cls, a, b):
        """
        Compare 2 elements assumed to be of same type
        :param a: Element
        :param b: Element
        :return:
        """
        if a.type != b.type:
            # raise RuntimeError('Cannot compare 2 elements of different type')
            return a.type - b.type
        if a.type == 1 or a.type == 2:  # date or number
            if a.value == b.value:
                return 0
            elif a.value < b.value:
                return -1
            return +1
        else:  # string
            return Element.compare_string(a.value, b.value)
        # default behavior fall back
        return 0


class MatchResult:
    elements = []
    type_sequence = ""

    def __init__(self, elements):
        self.elements = elements
        self.type_sequence = '-'.join(map(lambda e: str(e.type), elements))


class SequenceMatcher:
    # pattern index = 0|1:      date
    # pattern index = 2|3|4:    number
    # pattern index = 5:        alphabet
    def __init__(self):
        pass

    PATTERN = RE.compile(
        '(\d{4}[-]\d{2}[-]\d{2})|(\d{4}[/]\d{2}[/]\d{2})|([-]?\d+\.\d+)|([-]?\.\d+)|([-]?\d+)|([A-z]+)',
        RE.IGNORECASE)

    @classmethod
    def match(cls, str):
        """
        :return: list of Element as they appears in str by matching str left->right using the matching priority defined
        in PATTERN
        """
        matches = SequenceMatcher.PATTERN.findall(str)
        list = []
        for tuple in matches:
            for idx, val in enumerate(tuple):
                if val:
                    if 0 <= idx <= 1:  # date
                        list.append(Element.as_date(val))
                    elif 2 <= idx <= 4:  # number
                        list.append(Element.as_number(val))
                    else:  # simple string
                        list.append(Element.as_string(val))
                    break
        return MatchResult(list)


class CustomStringComparator:

    def __init__(self):
        pass

    @classmethod
    def compare(cls, a, b):
        if a == b:
            return 0
        matcha = SequenceMatcher.match(a)
        matchb = SequenceMatcher.match(b)
        if matcha.type_sequence != matchb.type_sequence:
            return Element.compare_string(matcha.type_sequence, matchb.type_sequence)
        return CustomStringComparator.compare_element_wise(matcha.elements, matchb.elements)

    @classmethod
    def compare_element_wise(cls, la, lb):
        for idx in range(min(len(la), len(lb))):
            a = la[idx]
            b = lb[idx]
            vs = Element.compare(a, b)
            if vs != 0:
                return vs
        # default behavior fall back
        if len(la) == len(lb):
            return 0
        elif len(la) < len(lb):
            return -1
        return +1


def sort_string(list):
    return sorted(list, cmp=CustomStringComparator.compare)


# select default test case here
list = []
while True:
    testcase = raw_input("Choose test case[1-8] (0 to quit): ")
    testcase = int(testcase)
    if testcase == 0:
        break
    if testcase == 1:
        # number
        list = ['10', '.2', '-1', '-2.4', '2']
    if testcase == 2:
        # date
        list = ['2017-01-01', '2016/10/10', '2016-10-12']
    if testcase == 3:
        # alphabet
        list = ['Apple', 'Watermelon', 'bacon']
    if testcase == 4:
        # mix - consistent types
        list = ['abc123', 'def45', 'abc45']
    if testcase == 5:
        # mix - consistent types
        list = ['started on 2016-01-02', 'ended on 2017-01-05', 'Ended on 2016-01-02', 'ended ON 2017-02-05']
    if testcase == 6:
        # mix - inconsistent types
        list = ['Valentine 2017-02-14', 'a200', 'a100', 'abcd 2016/01/01', 'bacon256', 'def45', '321apple',
                '2017/01/23 special', '20Watermelon']
    if testcase == 7:
        # mix - inconsistent types
        list = ['Valentine 2017/02/14 200', '2017/03/14 is Valentine', 'Ended 2017/02/15 300']
    if testcase == 8:
        # mix - inconsistent types
        list = ['abc 123', 'abc', 'abc 123 2017/02/23']

    print 'before: ' + str(list)
    list = sort_string(list)
    print 'after:  ' + str(list)
