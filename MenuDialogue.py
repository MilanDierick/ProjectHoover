import os
from enum import Enum


class MenuState(Enum):
    OVERVIEW = 0
    SCAN_CONFIGURATION = 1


class ScanParameters:
    def __init__(self):
        self.scan_mode: int = 0
        self.scan_amount: int = 0
        self.is_configured: bool = False


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_int_from_input(min_value, max_value, message, fail_message="Please enter a valid number."):
    while True:
        try:
            print(message)
            value = int(input(fail_message))

            if min_value <= value <= max_value:
                return value
            else:
                print(fail_message)
        except ValueError:
            print(fail_message)


def print_overview():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("####################")
    print("#  Project Hoover  #")
    print("####################")
    print("\n")
    print("Below you will find a list of available commands.")
    print("Type the number of the command you wish to execute and press enter.\n")
    print("1. Configure a new scan.")


def print_configure_new_scan():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Configure a new scan.")
    print("=====================\n")
    print("1. Individual power ranking.")


# def print_configure_new_scan_incorrect_input():
#     print("\033[2J\033[1;1H")  # Clear the console screen
#     print("Invalid input. Please enter a valid number.\n")
#     print("Configure a new scan.")
#     print("=====================\n")
#     print("1. Individual power ranking.")

class MenuDialogue:
    def __init__(self):
        self.state: MenuState = MenuState.OVERVIEW

    def switch_state(self, state):
        self.state = state

    def handle_state(self):
        if self.state == MenuState.OVERVIEW:
            self.handle_overview()
        elif self.state == MenuState.SCAN_CONFIGURATION:
            return self.handle_configure_new_scan()

    def handle_overview(self):
        input_value: int = -1

        os.system('cls' if os.name == 'nt' else 'clear')
        print_overview()

        # Ask for input from the user, and keep asking until a valid input is given
        while input_value < 1 or input_value > 1:
            try:
                input_value = int(input("\n\nPlease enter the number of the type of scan you would like to execute: "))

            except ValueError:
                input_value = -1

        if input_value == 1:
            self.switch_state(MenuState.SCAN_CONFIGURATION)

    def handle_configure_new_scan(self):
        input_value: int = -1
        scan_parameters: ScanParameters = ScanParameters()

        print_configure_new_scan()

        # Ask for input from the user, and keep asking until a valid input is given
        while input_value < 1 or input_value > 1:
            try:
                input_value = int(
                    input("\n\nPlease enter the number of the type of scan you would like to execute (1-1): "))

            except ValueError:
                input_value = -1

        scan_parameters.scan_mode = input_value
        input_value = -1

        # Ask for input from the user, and keep asking until a valid input is given
        while input_value < 1 or input_value > 1000:
            try:
                input_value = int(
                    input("\n\nPlease enter the amount of player profiles you would like to scan (1-1000): "))

            except ValueError:
                input_value = -1

        scan_parameters.scan_amount = input_value
        input_value = -1

        scan_parameters.is_configured = True
        return scan_parameters
