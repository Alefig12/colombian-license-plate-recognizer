import numpy as np
import cv2
import pytesseract
import imutils
from imutils import contours
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'



class PLR:
    def __init__(self, lower=np.uint8([5, 90 , 90]), upper=np.uint8([51, 255, 255]), dim=(500, 200), plate = None):
        self.lower = lower
        self.upper = upper
        self.dim = dim
        self.plate = plate

    def __convertHSV(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    def __findCountours(self, f_type, img):
        cnts = cv2.findContours(img, f_type, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        return cnts

    def __getBiggestCountour(self, cnts):
        return sorted(cnts, key=cv2.contourArea, reverse=True)[0]

    def __findByColorRange(self, img, lower, upper):

        return cv2.inRange(img, lower, upper)


    def __rezise(self, img, dim):
        return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    def __invertImg(self, img):
        return cv2.bitwise_not(img)

    def __sortLeftToRight(self, cnts):
        (cnts, _) = contours.sort_contours(cnts, method="left-to-right")
        return cnts

    def __scaleImg(self, img, scale_percent):

        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        newimg = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return newimg

    def __dilate_erode(self, img, kernel):

        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)

        return img

    def __applyBlurThreshold(self, img):

        return cv2.threshold(cv2.medianBlur(img, 5), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    def __cropPlate(self, img, cnts):
        x, y, w, h = cv2.boundingRect(cnts)
        cropped = img[y:y+h, x:x+w]
        return cropped

    def __splitCharacters(self, img):

        # Find character contours and sort them from the left.
        cnts = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

 

        (cnts, _) = contours.sort_contours(cnts, method="left-to-right")
        charsImg = []

        # Select each countour based on their area, perimeter and ratio. This should filter the countours that aren't characters.
        for c in cnts:
            area = cv2.contourArea(c)
            perimeter = cv2.arcLength(c, True)
            x, y, w, h = cv2.boundingRect(c)
            char = 255 - img[y:y+h, x:x+w]
            ratio = char.shape[0]/char.shape[1]
            if area > 2000 and perimeter < 650 and ratio > 1.2 and ratio < 2.2:
                charsImg.append(char)

        return charsImg

    def __applyFilters(self, char):

        # Make character image bigger

        char = self.__scaleImg(char, 130)

        # Draw a 25px white border on all sides
        char = cv2.copyMakeBorder(
            char, 25, 25, 25, 25, cv2.BORDER_CONSTANT, value=(255, 255, 255))

        # Dilate and erode image
        kernel = np.ones((1, 1), np.uint8)
        char = self.__dilate_erode(char, kernel)
        char = self.__applyBlurThreshold(char)

        return char

    def __readImage(self, img):
        return pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 10')

    def readPlate(self, img):

        # Obtaining the cropped license plate from image
        original = img.copy()
        imgHSV = self.__convertHSV(img)
        mask = self.__findByColorRange(imgHSV, self.lower, self.upper)



        cnts = self.__findCountours(cv2.RETR_EXTERNAL, mask)
        cnts = self.__getBiggestCountour(cnts)
        cropped = self.__cropPlate(original, cnts)

       
        
        # pre-process image for OCR
        resized = self.__rezise(cropped, self.dim)

        self.plate = resized

        imgHSV = self.__convertHSV(resized)
        mask = self.__findByColorRange(imgHSV, self.lower, self.upper)
        mask = self.__invertImg(mask)

        # Find and split plate characters
        characters = self.__splitCharacters(mask)

        # Apply border, filters and blur to each character
        i = 0
        


        for c in characters:
            characters[i] = self.__applyFilters(c)
            i += 1



        #Read each character image with tesseract
        text = ''
        for c in characters:
            
            text+= self.__readImage(c).strip()
            
        return text