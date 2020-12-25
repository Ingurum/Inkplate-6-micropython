import os


def exists(path):
    '''
    Return True if the path exists.
    '''
    try:
        os.stat(path)
        return True
    except OSError:
        return False
