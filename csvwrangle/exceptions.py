class CSVWrangleError(Exception):
    pass


class InvalidOperationName(KeyError, CSVWrangleError):
    pass


class MissingAssignment(CSVWrangleError):
    pass
