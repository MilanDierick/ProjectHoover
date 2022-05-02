import time
from datetime import date

import cv2
import pyperclip as pyperclip
import pytesseract
from xlwt import Workbook, XFStyle, Font

from Emulator import Emulator, tap_profile, tap_rankings, tap_individual_power, tap_profile_close, tap_copy_gov_name
from Player import Player

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

Y = [450, 615, 775, 935]

today = date.today()

wb = Workbook()
sheet1 = wb.add_sheet(str(today))
style = XFStyle()
font = Font()
font.bold = True
style.font = font

sheet1.write(0, 0, 'Governor ID', style)
sheet1.write(0, 1, 'Governor Name', style)
sheet1.write(0, 2, 'Alliance Tag', style)
sheet1.write(0, 3, 'Alliance Name', style)
sheet1.write(0, 4, 'Power', style)
sheet1.write(0, 5, 'Kill Points', style)

if __name__ == '__main__':
    emulator = Emulator()
    emulator.connect()

    for index in range(20):
        if index < 4:  # If we are selecting one of the first 4 players, we want use pre-defined coordinates
            emulator.tap(460, Y[index])
        else:
            emulator.tap(460, 935)

        time.sleep(0.5)  # Wait for the player profile to load

        with open('gov_info.png', 'wb') as screenshot:
            screenshot.write(emulator.screenshot())

        image = cv2.imread('gov_info.png')

        tap_copy_gov_name(emulator)
        time.sleep(0.5)

        gov_name = pyperclip.paste()

        try:
            player = Player(gov_name, image)
        except:
            player = Player(gov_name, image)

        print(player)
        player.save_to_sheet(sheet1, index)

        tap_profile_close(emulator)
        time.sleep(0.5)

    wb.save('gov_info.xls')
