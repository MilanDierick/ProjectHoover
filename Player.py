import cv2
import pytesseract


class Player:
    def __init__(self, gov_name, image_stream):
        import numpy as np

        # Image data
        _bytes_as_np_array = np.frombuffer(image_stream, dtype=np.uint8)
        self.image = cv2.imdecode(_bytes_as_np_array, cv2.IMREAD_COLOR)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Player information
        self.governor_id = int(self._parse_number(1240, 380, 300, 50))
        self.governor_name = gov_name
        self.alliance_tag, self.alliance_name = self._parse_text(1020, 580, 400, 60, True)

        # Player statistics
        self.power = int(self._parse_number(1450, 580, 300, 60))
        self.kills = int(self._parse_number(1815, 580, 300, 60))

    def _parse_number(self, x, y, w, h):
        _image = self.image[y:y + h, x:x + w]
        _image = cv2.threshold(_image, 145, 255, cv2.THRESH_OTSU)[1]

        try:
            data = pytesseract.image_to_string(_image, lang='eng',
                                               config="--psm 7, -c tessedit_char_whitelist=0123456789")
            print(data.strip())
            cv2.imshow("img", _image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return data.strip()
        except ValueError:
            cv2.imshow("img", _image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def _parse_text(self, x, y, w, h, parsing_alliance=False):
        _image = self.image[y:y + h, x:x + w]
        _image = cv2.threshold(_image, 145, 255, cv2.THRESH_OTSU)[1]

        try:
            data = pytesseract.image_to_string(_image, lang='eng', config="--psm 7")

            if parsing_alliance:
                if data.find("-") != -1:
                    return {"-", "-"}
                print(data.strip().split("]", 1))
                return data.strip().split("]", 1)

            print(data.strip())
            return data.strip()
        except ValueError:
            print(data)
            cv2.imshow("img", _image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def __str__(self):
        return "Governor ID: " + str(self.governor_id) + "\n" + \
               "Governor Name: " + self.governor_name + "\n" + \
               "Alliance Tag: " + self.alliance_tag + "\n" + \
               "Alliance Name: " + self.alliance_name + "\n" + \
               "Power: " + str(self.power) + "\n" + \
               "Kills: " + str(self.kills) + "\n"
