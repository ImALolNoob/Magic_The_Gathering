import re
import sqlite3
import time
from pprint import pprint

from sql_queries import connect_to_database, get_unique_set_codes, get_card_info, select_card_identifiers
from configs import *
import cv2
from colorama import Fore, Back, Style

print(Fore.RED + Back.GREEN + 'Hello, World!' + Style.RESET_ALL)
import random
from PIL import Image, ImageDraw
import pytesseract
import os

start_time = time.time()
# If you're on Windows, you will need to point pytesseract to the path
# where you installed Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Specify the directory containing images
image_dir = 'images'
files = os.listdir(image_dir)
random.shuffle(files)


def check_words_in_string(words, string_to_check):
    present_words = []
    for word in words:
        if word.lower() in string_to_check.lower():
            present_words.append(word)
    return present_words


def extract_info(text):
    # Split the text into lines
    matches = []
    patterns = [
        r'(\d+)/(\d+)\s+([A-Za-z])',  # 11/11 U
        r'([A-Za-z])\s+(\d+)\/(\d+)',  # U 11/11
        r'(\d+)\/(\d+)'  # 11/11

    ]

    lines = text.split('\n')

    results = []

    for line in lines:
        for pattern in patterns:
            matches = re.findall(pattern, line)
            if matches:
                results.extend(matches)

    return results


con = connect_to_database()
unique_set_codes = get_unique_set_codes(con)
print(unique_set_codes)


# Iterate through all files in the shuffled list

def image_check_full_image(filename):
    img = Image.open(os.path.join(image_dir, filename))
    width, height = img.size
    text_boxes = pytesseract.image_to_boxes(img)

    # Create a drawing object
    draw = ImageDraw.Draw(img)

    for box in text_boxes.splitlines():
        # Extract box coordinates and letter
        letter, x1, y1, x2, y2, *_ = box.split()
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        # Draw an 8x8 box around each letter
        draw.rectangle([x1 - 8, height - y2 - 8, x2 + 8, height - y1 + 8], outline="red")

    img.show()
    fullimagetext = pytesseract.image_to_string(img)
    pprint(fullimagetext)
    return fullimagetext


def image_search_bottom(filename):
    img = Image.open(os.path.join(image_dir, filename))
    width, height = img.size

    # Define the region of interest (bottom 20% of the image)
    roi_top = int(0.9 * height)
    roi_bottom = height
    roi_left = 0
    roi_right = width

    # Create a copy of the image to draw on
    img_with_border = img.copy()
    draw = ImageDraw.Draw(img_with_border)

    # Draw a border around the region of interest
    border_width = 8
    draw.rectangle([roi_left, roi_top, roi_right, roi_bottom], outline="red", width=border_width)

    # Perform OCR only on the region of interest
    roi = img.crop((roi_left, roi_top, roi_right, roi_bottom))
    text = pytesseract.image_to_string(roi)
    # print("-+-+-",Fore.LIGHTCYAN_EX, text,Fore.RESET)
    # roi.show()
    return text


counter = 0
for filename in files:
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # text = image_check_full_image(filename)
        text = image_search_bottom(filename)
        print("=============== \n",
              Fore.BLACK, filename, Fore.RESET)
        present_setCode = check_words_in_string(unique_set_codes, text)
        # present_words = check_words_in_string(card_type_words, text)
        present_card_max_num = extract_info(text)
        print(Fore.GREEN, text, Fore.RESET)
        # print(Fore.BLUE, present_setCode, Fore.CYAN, present_card_max_num, Fore.RESET)
        counter = counter + 1
        if len(present_card_max_num) > 0 and len(present_setCode) > 0:
            for cardnum in present_card_max_num:
                for setcode in present_setCode:
                    # print("look at meeee", cardnum, setcode)
                    card_info = get_card_info(setcode, cardnum[0])

                    # temp = select_card_identifiers(con,card_info['id'])
                    # print(f"TEMPPPP: {}")

                    try:
                        print("TESTTTTTt ======== ", card_info['data'][0]['id'])
                    except Exception:
                        print(card_info)

        # time.sleep(1)
end_time = time.time()
elapsed_time = end_time - start_time

print("Elapsed time:", elapsed_time, "seconds")
