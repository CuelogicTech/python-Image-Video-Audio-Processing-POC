import cv2
import sys
import os
from PIL import Image
from pytesseract import *
from subprocess import check_output
from textblob import TextBlob
from django.conf import settings

class ImageProcessing(object):

    def __init__(self, image):

        self.imagePath = image

        if self.imageValidation():
            try:
                self.imgOpen = Image.open(self.imagePath)
            except:
                return "Image could not open."

    def faceDetection(self):

        face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')
        face_detect = {}
        img = cv2.imread(self.imagePath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.2, 3, minSize=(20, 20), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # cv2.imshow('img',img)
        imageFilename = os.path.basename(self.imagePath)
        if not os.path.exists(settings.MEDIA_ROOT + 'face_detect/'):
            os.makedirs(settings.MEDIA_ROOT + 'face_detect/', 777)

        if len(faces) > 0:
            cv2.imwrite(settings.MEDIA_ROOT + 'face_detect/' + imageFilename, img)
            face_detect["result_image"] = settings.MEDIA_URL + 'face_detect/' + imageFilename

        face_detect["face_count"] = len(faces)
        # cv2.waitKey(0)

        return face_detect

    def extract_text(self):

        text = image_to_string(self.imgOpen)

        language = ""
        if len(text) > 3 != "":
            languageCode = self.detectLanguage(text)
            
            if languageCode != "" and str(languageCode) != "None":
                language = self.languageName(languageCode)

        textinfo = {}
        textinfo["text"] = text
        textinfo["language"] = language
        return textinfo

    def getImageColor(self):

        img_rgb = self.imgOpen.convert('RGB')

        colors = {}
        for color in img_rgb.getdata():
            colors[color] = colors.get(color, 0) + 1

        return self.getColorPercentage(colors)

    def checkDuplicateImage(self, compare_path):

        images_compare = check_output(["python", "ssim", self.imagePath, compare_path+"/*"])

        duplicateImages = []
        split_result = images_compare.split(' - ')

        if len(split_result) > 0:

            for image_path in split_result:
                splitImagePath = image_path.split('\n')

                if len(splitImagePath) == 2:
                    duplicateImg = splitImagePath[0].split(':')

                    if len(duplicateImg) > 0 and len(duplicateImg) == 2:

                        duplicateImgRatio = float(duplicateImg[1]) * 100
                        if duplicateImgRatio >= 50:
                            duplicateImages.append(duplicateImg[0])

        return duplicateImages

    def getColorPercentage(self, colors):

        red_color = yellow_color = orange_color = green_color = blue_color = white_color = pink_color = black_color = grey_color = purple_color = brown_color = 0

        for bgr_code in colors.keys():
            # BGR RGB
            if bgr_code[0] > 150 and bgr_code[1] < 50 and bgr_code[2] < 50:
                red_color += 1
            elif bgr_code[0] > 200 and bgr_code[1] > 200 and bgr_code[2] < 100:
                yellow_color += 1
            elif bgr_code[0] > 200 and bgr_code[1] > 100 and (bgr_code[2] < 200 and bgr_code[2] < 50):
                orange_color += 1
            elif bgr_code[0] < 50 and bgr_code[1] > 150 and bgr_code[2] < 50:
                green_color += 1
            elif bgr_code[0]< 50 and bgr_code[1] < 50 and bgr_code[2] > 150:
                blue_color += 1
            elif bgr_code[0] > 240 and bgr_code[1] > 240 and bgr_code[2] > 240:
                white_color += 1
            elif bgr_code[0] < 40 and bgr_code[1] < 40 and bgr_code[2] < 40:
                black_color += 1
            elif bgr_code[0] > 150 and bgr_code[1] < 50 and bgr_code[2] > 150:
                pink_color += 1
            elif (bgr_code[0] > 40 and bgr_code[0] < 240) and (bgr_code[1] > 40 and bgr_code[1] < 240) and (bgr_code[2] > 40 and bgr_code[2] < 240):
                grey_color += 1
            elif (bgr_code[0] > 80 and bgr_code[0] < 120) and (bgr_code[1] > 0 and bgr_code[1] < 110) and bgr_code[2] > 180:
                purple_color += 1
            elif (bgr_code[0] > 70 and bgr_code[0] < 120) and bgr_code[1] < 50 and bgr_code[2] < 50:
                brown_color += 1


        total_color = red_color + yellow_color + orange_color + green_color + blue_color + white_color + pink_color + black_color + grey_color + purple_color + brown_color

        clorsPercentage = {}
        clorsPercentage["red"] = round((red_color / float(total_color)) * 100, 4)
        clorsPercentage["yellow"] = round((yellow_color / float(total_color)) * 100, 4)
        clorsPercentage["orange"] = round((orange_color / float(total_color)) * 100, 4)
        clorsPercentage["green"] = round((green_color / float(total_color)) * 100, 4)
        clorsPercentage["blue"] = round((blue_color / float(total_color)) * 100, 4)
        clorsPercentage["white"] = round((white_color / float(total_color)) * 100, 4)
        clorsPercentage["pink"] = round((pink_color / float(total_color)) * 100, 4)
        clorsPercentage["black"] = round((black_color / float(total_color)) * 100, 4)
        clorsPercentage["grey"] = round((grey_color / float(total_color)) * 100, 4)
        clorsPercentage["purple"] = round((purple_color / float(total_color)) * 100, 4)
        clorsPercentage["brown"] = round((brown_color / float(total_color)) * 100, 4)

        return sorted(clorsPercentage.items(), key=lambda (k,v): (v,k))[::-1]

    def imageValidation(self):

        filepath, filename = os.path.split(self.imagePath)
        shortname, extension = os.path.splitext(filename)
        extensionlist = ['.jpg', '.png', '.gif', '.jpeg']

        if extension.lower() in extensionlist:
            return True
        else:
            return False

    def detectLanguage(self, text):

        language = TextBlob(text.decode('utf-8').strip())
        return language.detect_language()

    def languageName(slef, languageCode):

        languageDict = {'af' : 'Afrikaans', 'sq' : 'Albanian', 'ar' : 'Arabic', 'hy' : 'Armenian', 'az' : 'Azerbaijani', 'eu' : 'Basque', 'be' : 'Belarusian', 'bn' : 'Bengali', 'bs' : 'Bosnian', 'bg' : 'Bulgarian', 'ca' : 'Catalan', 'ceb' : 'Cebuano', 'ny' : 'Chichewa', 'zh-CN' : 'Chinese', 'zh-TW' : 'Chinese', 'hr' : 'Croatian', 'cs' : 'Czech', 'da' : 'Danish', 'nl' : 'Dutch', 'en' : 'English', 'eo' : 'Esperanto', 'et' : 'Estonian', 'fil' : 'Filipino', 'tl' : 'Finnish', 'fr' : 'French', 'gl' : 'Galician', 'ka' : 'Georgian', 'de' : 'German', 'el' : 'Greek', 'gu' : 'Gujarati', 'ht' : 'Haitian', 'ha' : 'Hausa', 'iw' : 'Hebrew', 'hi' : 'Hindi', 'hmn' : 'Hmong', 'hu' : 'Hungarian', 'is' : 'Icelandic', 'ig' : 'Igbo', 'id' : 'Indonesian', 'ga' : 'Irish', 'it' : 'Italian', 'ja' : 'Japanese', 'jw' : 'Javanese', 'kn' : 'Kannada', 'kk' : 'Kazakh', 'km' : 'Khmer', 'ko' : 'Korean', 'lo' : 'Lao', 'la' : 'Latin', 'lv' : 'Latvian', 'lt' : 'Lithuanian', 'mk' : 'Macedonian', 'mg' : 'Malagasy', 'ms' : 'Malay', 'ml' : 'Malayalam', 'mt' : 'Maltese', 'mi' : 'Maori', 'mr' : 'Marathi', 'mn' : 'Mongolian', 'my' : 'Myanmar', 'ne' : 'Nepali', 'no' : 'Norwegian', 'fa' : 'Persian', 'pl' : 'Polish', 'pt' : 'Portuguese', 'pa' : 'Punjabi', 'ro' : 'Romanian', 'ru' : 'Russian', 'sr' : 'Serbian', 'st' : 'Sesotho', 'si' : 'Sinhala', 'sk' : 'Slovak', 'sl' : 'Slovenian', 'so' : 'Somali', 'es' : 'Spanish', 'su' : 'Sudanese', 'sw' : 'Swahili', 'sv' : 'Swedish', 'tg' : 'Tajik', 'ta' : 'Tamil', 'te' : 'Telugu', 'th' : 'Thai', 'tr' : 'Turkish', 'uk' : 'Ukrainian', 'ur' : 'Urdu', 'uz' : 'Uzbek', 'vi' : 'Vietnamese', 'cy' : 'Welsh', 'yi' : 'Yiddish', 'yo' : 'Yoruba', 'zu' : 'Zulu', 'None' : ''}
        
        return languageDict[languageCode]
