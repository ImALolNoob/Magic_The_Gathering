import re
import sqlite3
import time
from pprint import pprint

from sql_queries import connect_to_database, get_unique_set_codes, get_card_info, search_cards_by_scryfall_id
from configs import *
import cv2
from colorama import Fore, Back, Style

print(Fore.RED + Back.GREEN + 'Hello, World!' + Style.RESET_ALL)
import random
from PIL import Image, ImageDraw
import pytesseract
import os
from tqdm import tqdm

from sys import platform

if platform == "linux" or platform == "linux2":
    print("linux Userrrr Ayyy Legend")
elif platform == "win32":
    print("windows user ewwww")
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

start_time = time.time()
# If you're on Windows, you will need to point pytesseract to the path
# where you installed Tesseract


# Specify the directory containing images
image_dir = 'images'
files = os.listdir(image_dir)
random.shuffle(files)


def check_words_in_string(words, string_to_check):
    present_words = []
    if string_to_check is not None:  # Check if string_to_check is not None
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
    try:
        img = Image.open(os.path.join(image_dir, filename))
    except Exception:
        return False
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
    ret_text = pytesseract.image_to_string(roi)

    # Remove "EN.*" in a line, where "EN" comes after a space (first space is after the set code)
    # regex:
    # - positive lookahead (?=) matches _after_ this group (so set code isn't deleted)
    # - \s matches space
    # - .* before EN as there may be trash characters picked up between the set code and "EN"
    # NOTE: Not fully accurate but thus far has not removed successful cases
    ret_text = re.sub(r"(?=\s).*EN.*", "", ret_text)

    # print("-+-+-",Fore.LIGHTCYAN_EX, ret_text,Fore.RESET)
    # roi.show()
    return ret_text


counter_succ = 0
counter_fail = 0
api_id = ""
for filename in tqdm(files, position=0):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # text = image_check_full_image(filename)
        text = image_search_bottom(filename)
        if not text:
            pass
        print("=============== \n",
              Fore.BLACK, filename, Fore.RESET)
        present_setCode = check_words_in_string(unique_set_codes, text)
        # present_words = check_words_in_string(card_type_words, text)
        present_card_max_num = extract_info(text)
        # print(Fore.GREEN, text, Fore.RESET)
        # print(Fore.BLUE, present_setCode, Fore.CYAN, present_card_max_num, Fore.RESET)
        if len(present_card_max_num) > 0 and len(present_setCode) > 0:
            for cardnum in present_card_max_num:
                for setcode in present_setCode:
                    # print("look at meeee", cardnum, setcode)
                    card_info = get_card_info(setcode, cardnum[0])

                    try:
                        api_id = card_info['data'][0]['id']
                        # print("api_id")
                    except Exception:
                        api_id = False
                    # print(card_info)
                    if api_id:

                        # print(f"API Id Requested: {api_id}")
                        UUID = search_cards_by_scryfall_id(con, api_id)[0]
                        print("AAAAAAA", UUID, filename)
                        if UUID + ".jpg" == filename:
                            counter_succ += 1
                            print("MATCHINGGGGGGGG!!!!!!!!!!!!")
                    else:
                        counter_fail += 1

        # time.sleep(1)
end_time = time.time()
elapsed_time = end_time - start_time

print("Elapsed time:", elapsed_time, "seconds")
print(f"success: {counter_succ}")
print(f"failed:  {counter_fail}")
