from adb_shell.adb_device import AdbDeviceTcp


# Helper functions
def tap_profile(emulator):
    emulator.tap(30, 30)


def tap_rankings(emulator):
    emulator.tap(330, 400)


def tap_individual_power(emulator):
    emulator.tap(250, 310)


class Emulator:
    def __init__(self):
        self.device = AdbDeviceTcp(host='localhost', port=5555)

    def connect(self):
        print('Connecting to emulator...')
        self.device.connect()

        if not self.is_connected():
            print("Failed to establish connection to the emulator.")
        else:
            print("Successfully connected to the emulator.")

    def is_connected(self):
        return self.device.available

    def tap(self, x, y):
        self.device.shell('input tap {} {}'.format(x, y))

    def screenshot(self):
        return self.device.exec_out(command='screencap -p', decode=False)


