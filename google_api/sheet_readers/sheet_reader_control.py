from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta


class SheetReaderContext:

    @staticmethod
    def determine_reader(sheet_type):
        if sheet_type == "assignment":
            return AssignmentSheetReader()


class SheetReaderBase(ABC):

    def __init__(self):
        self.row_info = {}

    @abstractmethod
    def should_notify_user(self, row) -> bool:
        pass

    def _read_row_information(self, row, ATTRIBUTES):

        self.row_info = {}
        print(f"DEBUG -- Row -- {row}")
        if row:
            print(f"Attributes: {len(ATTRIBUTES)}")
            column = 0
            for category in ATTRIBUTES:
                print(f"Column: {column}")
                self.row_info[category] = row[column]
                column += 1
        else:
            print("Row empty!")

    @abstractmethod
    def create_message(self, row) -> dict:
        pass

    @abstractmethod
    def get_subject(self):
        pass

    @abstractmethod
    def get_title(self, notify_counter):
        pass

    @abstractmethod
    def get_links(self) -> dict:
        pass


class AssignmentSheetReader(SheetReaderBase):

    # Attributes need to be in order that they appear in the document
    ATTRIBUTES = ['class_code', 'assignment', 'status', 'weight', 'time', 'start_date', 'due_date']
    DATE_TEMPLATE = '%a, %b %d, %Y'

    def should_notify_user(self, row) -> bool:
        self._read_row_information(row, self.ATTRIBUTES)

        date_valid, date_diff = self._calculate_date_diff()
        if date_valid:
            # If the date has not already passed
            if date_diff >= 0:
                return self._due_date_close(date_diff)
            else:
                return False
        else:
            return False

    def _calculate_date_diff(self) -> (bool, int):
        # If the due date does not exist
        if self.row_info.get('due_date', None) is None:
            print(f"DATE NOT VALID! Got: {self.row_info.get('due_date', None)} Expected date like 'Wed, Jan 25, 2023'")
            return False, -1
        try:
            today = date.today()
            due_date = datetime.strptime(self.row_info['due_date'], self.DATE_TEMPLATE).date()
            return True, (due_date - today).days
        except ValueError:
            print(f"DATE NOT VALID! Got: {self.row_info['due_date']} Expected date like 'Wed, Jan 25, 2023'")
            return False, -1

    def _due_date_close(self, date_diff) -> bool:
        days_to_notify = [5, 3, 1]
        return self.row_info['status'] != 'Done' and date_diff in days_to_notify

    def create_message(self, row) -> list:
        message_info = []
        self._read_row_information(row, self.ATTRIBUTES)
        date_valid, date_diff = self._calculate_date_diff()
        if date_valid:
            message_str = f"{self.row_info['class_code']} assignment --> {self.row_info['assignment']} " \
                          f"is due in {date_diff} days ({self.row_info['due_date']})! It is worth <b>[{self.row_info['weight']}]</b>"
            message_info.append(message_str)
        return message_info

    def get_subject(self):
        return "Assignment(s) due!"

    def get_title(self, notify_counter):
        return f"You have {notify_counter} assignments/midterms due soon!"

    def get_links(self) -> dict:
        return {"Brightspace": "https://brightspace.carleton.ca/d2l/home"}

