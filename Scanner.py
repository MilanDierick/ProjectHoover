import os
import time
from datetime import date

import cv2
import pyperclip
from xlwt import Workbook, XFStyle, Font

from Emulator import Emulator, tap_profile_close, tap_copy_gov_name
from MenuDialogue import ScanParameters, clear_console
from Player import Player

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


def add_player_to_sheet(player: Player, row):
    sheet1.write(row, 0, player.governor_id)
    sheet1.write(row, 1, player.governor_name)
    sheet1.write(row, 2, player.alliance_tag)
    sheet1.write(row, 3, player.alliance_name)
    sheet1.write(row, 4, player.power)
    sheet1.write(row, 5, player.kills)


class Scanner:
    def __init__(self, scan_parameters: ScanParameters, emulator: Emulator):
        self.parameters = scan_parameters
        self.emulator = emulator
        self.players = []

    def execute(self):
        _y = [450, 615, 775, 935]  # Predefined y coordinates for the first 4 profiles
        _start_time = time.time()  # Keep track of when the scan started
        _last_time = time.time()  # Keep track of the last time a profile was captured
        _time_per_profile = []  # Keep track of the time it takes to capture each profile

        # Loop through the profiles and capture them
        for index in range(self.parameters.scan_amount):
            y_pos = _y[index] if index < 4 else 1020
            _last_time = time.time() # Reset the last time a profile was captured
            self.emulator.tap(460, y_pos) # Tap the profile
            time.sleep(1.0) # Wait for the profile to load
            self._capture_profile()
            tap_profile_close(self.emulator)
            time.sleep(0.5) # Wait for the profile to close

            if len(_time_per_profile) > 10: # We only want to keep the time per profile for the last 10 profiles
                _time_per_profile.pop(0) # Remove the oldest entry from the list

            _time_per_profile.append(time.time() - _last_time) # Add the time it took to capture the profile to the list
            self.print_scan_progress(index, self.parameters.scan_amount, _start_time - time.time(), _time_per_profile)

    def _capture_profile(self):
        # with open('gov_info.png', 'wb') as screenshot:
        #     screenshot.write(self.emulator.screenshot())

        # image = cv2.imread(self.emulator.screenshot())
        image_stream = self.emulator.screenshot()
        tap_copy_gov_name(self.emulator)
        time.sleep(0.5) # Wait for the emulator to copy the governor name
        gov_name = pyperclip.paste()

        try:
            player = Player(gov_name, image_stream)
        except ValueError:
            print("Failed to parse player profile, trying again in 2 seconds.")
            time.sleep(2)
            # with open('gov_info.png', 'wb') as screenshot:
            #     screenshot.write(self.emulator.screenshot())
            image_stream = self.emulator.screenshot()
            player = Player(gov_name, image_stream)

        self.players.append(player)

    def print_scan_progress(self, scanned_players: int, total_players: int, time_since_start: float,
                            time_per_profile_collection: list):
        clear_console()
        print("Scanned {} out of {} players.".format(scanned_players, total_players))

        elapsed_time_minutes = int(time_since_start / 60)
        elapsed_time_seconds = int(time_since_start % 60)
        print("Elapsed time: {} minutes {} seconds.".format(elapsed_time_minutes, elapsed_time_seconds))

        if len(time_per_profile_collection) == 0:
            print("Average time per profile: N/A")
            print("Estimated time remaining: N/A")

        # Calculate the average elapsed time for the last 10 players scanned
        average_elapsed_time = sum(time_per_profile_collection) / len(time_per_profile_collection)
        average_elapsed_time_minutes = int(average_elapsed_time / 60)
        average_elapsed_time_seconds = int(average_elapsed_time % 60)
        print("Average time per profile: {} minutes {} seconds.".format(average_elapsed_time_minutes,
                                                                        average_elapsed_time_seconds))

        # Calculate the estimated time remaining
        estimated_time_remaining = (total_players - scanned_players) * average_elapsed_time
        estimated_time_remaining_minutes = int(estimated_time_remaining / 60)
        estimated_time_remaining_seconds = int(estimated_time_remaining % 60)
        print("Estimated time remaining: {} minutes {} seconds.".format(estimated_time_remaining_minutes,
                                                                        estimated_time_remaining_seconds))

        print("[{0:50s}] {1:.1f}%".format('#' * int(scanned_players / total_players * 50),
                                          scanned_players / total_players * 100))
