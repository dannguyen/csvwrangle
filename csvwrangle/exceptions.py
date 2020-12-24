class CSVWrangleError(Exception):
    pass


class InvalidOperationName(KeyError, CSVWrangleError):
    pass
