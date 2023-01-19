from abc import ABC, abstractmethod


class SheetReaderContext:

    @staticmethod
    def determine_reader(sheet_type):
        if sheet_type == "assigment":
            return AssignmentSheetReader()


class SheetReaderBase(ABC):

    @abstractmethod
    def should_notify_user(self, row) -> bool:
        pass

    def _read_row_information(self, row, ATTRIBUTES) -> dict:

        row_info = {}

        column = 0
        for category in ATTRIBUTES:
            row_info[category] = row[column]
            column += 1

        return row_info

    @abstractmethod
    def create_message(self, row) -> dict:
        pass

    @abstractmethod
    def get_subject(self):
        pass

    @abstractmethod
    def get_links(self) -> dict:
        pass


class AssignmentSheetReader(SheetReaderBase):

    # Attributes need to be in order that they appear in the document
    ATTRIBUTES = ['class_code', 'assignment', 'status', 'weight', 'time', 'start_date', 'due_date']

    def should_notify_user(self, row) -> bool:
        row_info = self._read_row_information(row, self.ATTRIBUTES)



        return False

    def create_message(self, row) -> dict:
        pass

    def get_subject(self):
        return "Assignment(s) due!"

    def get_links(self) -> dict:
        return {"Brightspace": "https://brightspace.carleton.ca/d2l/home"}

