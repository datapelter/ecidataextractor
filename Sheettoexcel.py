import cv2
import numpy as np
import pytesseract
import re
import cv2
import pandas as pd

def cleanStringEntry(textEntry):
    namestr = textEntry
    namestr = namestr.replace('#', '')
    namestr = namestr.replace(':', '')
    namestr = namestr.replace('.', '')
    namestr = namestr.lstrip()
    return namestr

def extract_dict_from_text(textstring):

    entry_dict = {}

    
    textstring = textstring.replace('\n', '#')
    # print(textstring)

    #name = name.replace('\n','')
    serial_number = re.search(r'\d+', textstring)
    entry_dict['serial_number'] = cleanStringEntry(serial_number.group())

    epic = re.search(r'[A-Z]{3}\d{7}', textstring)
    entry_dict['epic'] = epic.group()

    name = re.search(r'(?<=Name)(.*)(?=(Hus|Fat|Mot))', textstring)
    entry_dict['name'] = cleanStringEntry(name.group())

    gaurdian = re.search(r'(?<=\'s Name)(.*)(?=Hou)', textstring)
    entry_dict['guardian'] = cleanStringEntry(gaurdian.group())

    house = re.search(r'(?<=ber)(.*)(?=Age)', textstring)
    entry_dict['house'] = cleanStringEntry(house.group())

    age = re.search(r'(?<=ge)(.*)(?=Ge)', textstring)
    entry_dict['age'] = cleanStringEntry(age.group())
    
    gender = re.search(r'(?<=der)(.*)(?=(E|R))', textstring)
    if 'FEMAL' in gender.group():
        entry_dict['gender'] = 'FEMALE'
    else:
        entry_dict['gender'] = 'MALE'
 
    print(entry_dict)
    return(entry_dict)

img = cv2.imread(
    "./input/19.png")

box_height = 149
box_width = 375

first_rect_start_x = 53
first_rect_start_y = 86

result_array = [] 

for row in range(0, 10):
    for column in range(0, 3):
        rectx = first_rect_start_x + box_width * column
        recty = first_rect_start_y + box_height * row

        crop = img[recty:recty+box_height, rectx:rectx+box_width]
        cv2.imshow('Image', crop)
        text = pytesseract.image_to_string(crop)
        
        if len(text) >50:
            result = extract_dict_from_text(textstring=text)
            print (result)
            result_array.append(result)
        cv2.waitKey(0)

newdf = pd.DataFrame(result_array)
newdf.to_excel("result3.xlsx")

# box height is 145
# box width  is 375
