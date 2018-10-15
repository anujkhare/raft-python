# FIXME: This should be something that is easily extensible and can be changed by the users
class LogEntry:
    def __init__(self, index, term, data, *args, **kwargs) -> None:
        self.index = index
        self.term = term
        self.data = data


class Log:
    def __init__(self) -> None:
        self.entries = []

    def __len__(self) -> int:
        return len(self.entries)

    def append(self, entry: 'LogEntry') -> None:
        self.entries.append(entry)


