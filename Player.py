import pytesseract

from ImageUtilies import get_grayscale, thresholding

roi_gov_id = (1240, 380, 300, 40)
roi_gov_name = (1025, 425, 600, 60)
roi_alliance = (1035, 590, 400, 40)
roi_gov_power = (1450, 580, 300, 60)
roi_gov_kills = (1815, 580, 300, 60)


class Player:
    def __init__(self, gov_name, image):
        self.governor_id = 0
        self.governor_name = gov_name
        self.alliance_tag = ""
        self.alliance_name = ""
        self.power = 0
        self.kills = 0

        self.process_image(image)

    def process_image(self, image):
        image_grey = get_grayscale(image)

        gov_id_img = image_grey[roi_gov_id[1]:roi_gov_id[1] + roi_gov_id[3],
                     roi_gov_id[0]:roi_gov_id[0] + roi_gov_id[2]]
        alliance_img = image_grey[roi_alliance[1]:roi_alliance[1] + roi_alliance[3],
                       roi_alliance[0]:roi_alliance[0] + roi_alliance[2]]
        gov_power_img = image_grey[roi_gov_power[1]:roi_gov_power[1] + roi_gov_power[3],
                        roi_gov_power[0]:roi_gov_power[0] + roi_gov_power[2]]
        gov_kills_img = image_grey[roi_gov_kills[1]:roi_gov_kills[1] + roi_gov_kills[3],
                        roi_gov_kills[0]:roi_gov_kills[0] + roi_gov_kills[2]]

        gov_id_img = thresholding(gov_id_img)
        alliance_img = thresholding(alliance_img)
        gov_power_img = thresholding(gov_power_img)
        gov_kills_img = thresholding(gov_kills_img)

        self.governor_id = int(pytesseract.image_to_string(gov_id_img, config='-c tessedit_char_whitelist=0123456789'))
        alliance_name_and_tag = pytesseract.image_to_string(alliance_img)
        tag, name = alliance_name_and_tag.split("]")
        self.alliance_tag = tag[1:]
        self.alliance_name = name.strip()
        self.power = int(pytesseract.image_to_string(gov_power_img, config='-c tessedit_char_whitelist=0123456789'))
        self.kills = int(pytesseract.image_to_string(gov_kills_img, config='-c tessedit_char_whitelist=0123456789'))

    def save_to_sheet(self, sheet, index):
        sheet.write(index + 1, 0, self.governor_id)
        sheet.write(index + 1, 1, self.governor_name)
        sheet.write(index + 1, 2, self.alliance_tag)
        sheet.write(index + 1, 3, self.alliance_name)
        sheet.write(index + 1, 4, self.power)
        sheet.write(index + 1, 5, self.kills)

    def __str__(self):
        return "Governor ID: " + str(self.governor_id) + "\n" + \
               "Governor Name: " + self.governor_name + "\n" + \
               "Alliance Tag: " + self.alliance_tag + "\n" + \
               "Alliance Name: " + self.alliance_name + "\n" + \
               "Power: " + str(self.power) + "\n" + \
               "Kills: " + str(self.kills) + "\n"
