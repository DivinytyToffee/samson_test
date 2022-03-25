def reverse_string(string):
    return string[::-1]


def test_reverse_string(list_strings=None):
    if list_strings is None:
        list_strings = [
            'abbbccd',
            'privet',
            'temporary'
        ]
    for string in list_strings:
        print 'Default string - {0} \nReverse string - {1}'\
            .format(string, reverse_string(string))
