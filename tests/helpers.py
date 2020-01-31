import sys


def python_version_2():
    return sys.version_info[0] == 2 and sys.version_info[1] >= 7


def python_version_3():
    return sys.version_info[0] == 3 and sys.version_info[1] >= 2
