class Header:
    _level: int
    _title: str

    def __init__(self, level: int, title: str):

        if level < 0:
            raise ValueError("Hierarchical level can't be below zero!")

        if len(title) == 0:
            raise ValueError("Title can't be empty!")

        self._level = level
        self._title = title

    def get_level(self) -> int:
        return self._level

    def get_title(self) -> str:
        return self._title
