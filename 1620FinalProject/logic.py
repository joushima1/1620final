from PyQt6.QtWidgets import *
from guiproject import *


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
        sets up UI, declares variables, and connects buttons to functions
        """
        super().__init__()
        self.setupUi(self)
        self.jane_votes = 0
        self.john_votes = 0
        self.id_list = []
        self.submit_button.clicked.connect(lambda: self.submit())
        self.clear_button.clicked.connect(lambda: self.clear())
        self.voting_results_button.clicked.connect(lambda: self.voting_results())
        self.voting_results_button.setDisabled(True)

        self.group = QButtonGroup(self)
        self.group.addButton(self.john_rad_button)
        self.group.addButton(self.jane_rad_button)
        self.jane_rad_button.toggled.connect(lambda: self.check_buttons(self.jane_rad_button))
        self.john_rad_button.toggled.connect(lambda: self.check_buttons(self.john_rad_button))

        # if not id valid(own func), change popup txt return blank
        # own func data validation for 5-digit id
        # add clear button and func?

    def submit(self) -> None:
        """
        function to submit a users vote, also makes sure their inputs are valid
        """
        user_id = self.id_edit.text()

        if not (self.id_valid(user_id)):
            self.notification_label.setText('Enter a valid ID')
            self.notification_label.setStyleSheet("color: red;")
            return

        if user_id in self.id_list:
            self.notification_label.setText('Vote already submitted')
            self.notification_label.setStyleSheet("color: red;")
            return

        # self.id_list.append(user_id)

        if self.john_rad_button.isChecked():
            self.john_votes += 1
        elif self.jane_rad_button.isChecked():
            self.jane_votes += 1
        else:
            self.notification_label.setText('Please select a candidate')
            self.notification_label.setStyleSheet("color: red;")
            return

        self.id_list.append(user_id)

        self.notification_label.setText('Vote submitted')
        self.notification_label.setStyleSheet("")
        self.voting_results_button.setDisabled(False)

    def id_valid(self, id: str) -> bool:
        """
        function for making sure the ID is an int and 5 digits long
        :param id: the ID trying to be validated, it should be a string that can be converted into an integer
        :return: returns true if ID is a 5-digit integer, false otherwise
        """
        try:
            int(id)
            return len(id) == 5
        except ValueError:
            return False

    def clear(self) -> None:
        """
        clears ID input and label, unchecks radio buttons, and sets focus back to the id_edit box.
        """
        self.id_edit.clear()
        self.group.setExclusive(False)
        self.john_rad_button.setChecked(False)
        self.jane_rad_button.setChecked(False)
        self.group.setExclusive(True)
        self.notification_label.clear()
        self.id_edit.setFocus()

    def voting_results(self) -> None:
        """
        clears the id_edit box, displays the votes and winner of the election, as well as disabling everything.
        """
        self.id_edit.clear()
        self.notification_label.setStyleSheet("")
        if self.jane_votes > self.john_votes:
            self.notification_label.setText(
                f'Jane votes - {self.jane_votes}\n John votes - {self.john_votes}\n The winner of '
                f'the election is Jane!')
        elif self.john_votes > self.jane_votes:
            self.notification_label.setText(
                f'John votes - {self.john_votes}\n Jane votes - {self.jane_votes}\n The winner of '
                f'the election is John!')
        else:
            self.notification_label.setText(f'John votes - {self.john_votes}\n Jane votes - {self.jane_votes}\nThis '
                                            f'election has ended in a tie.')
        self.id_edit.setDisabled(True)
        self.submit_button.setDisabled(True)
        self.clear_button.setDisabled(True)
        self.john_rad_button.setCheckable(False)
        self.jane_rad_button.setCheckable(False)
        self.voting_results_button.setDisabled(True)

    def check_buttons(self, radioButton) -> None:
        """
        function added to uncheck the radio buttons using the clear() function
        :param radioButton: john_rad_button and jane_rad_button
        """
        for button in self.group.buttons():
            if button is not radioButton:
                button.setChecked(False)