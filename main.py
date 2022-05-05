import pytesseract

from Emulator import Emulator
from MenuDialogue import ScanParameters, print_overview, get_int_from_input
from Scanner import Scanner

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

emulator = Emulator()

def init():
    emulator.connect()


def main():
    print_overview()
    command_value = get_int_from_input(1, 1, "Please enter a valid command number.")

    if command_value == 1:
        scan_parameters = ScanParameters()

        scan_parameters.scan_mode = get_int_from_input(1, 1, "Please enter a valid scan mode: ")
        scan_parameters.scan_amount = get_int_from_input(1, 1000, "Please enter a valid amount of players to scan: ")

        scanner = Scanner(scan_parameters, emulator)
        scanner.execute()

        for player in scanner.players:
            print(player)


def cleanup():
    pass


if __name__ == '__main__':
    init()
    main()
    cleanup()

    # wb.save('gov_info.xls')
