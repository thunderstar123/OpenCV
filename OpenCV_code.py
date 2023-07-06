import zipfile

import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')


#unzip the file and assign each page elements to a variable in memory

cfile = 'readonly/images.zip'
zip_ref = zipfile.ZipFile(cfile, 'r')
#display(zip_ref.infolist())
zip_ref.extractall()
zip_ref.close()

#display each of the page image files for reference

file_names = ['a-0.png','a-1.png', 'a-10.png', 'a-11.png', 'a-12.png', 'a-13.png', 'a-2.png','a-3.png','a-4.png','a-5.png','a-6.png','a-7.png','a-8.png','a-9.png',]

#for name in file_names :
    #display(Image.open(name))

#search for occurances of a word on a page with Tesseract
def page_read(page, keyword) :
    '''Calls tesseract to search a page of text for the occurance of keyword
    
    Params:
        Page: filename in PNG
        Keyword: search string
        
    Returns: True or False '''    
    
    image = Image.open(page)
    text = pytesseract.image_to_string(image)
    
    text_no_break = text.replace('\n','')
    
    return keyword in text_no_break

#page_read('a-0.png', 'Christopher') 

#build a list of pages with the keyword
def keyword_page_list(file_names, keyword):
    '''Pass a page list and get a list of page files with keywords in return'''
    
    page_with_keyword = []
    
    for page in file_names :
        if page_read(page, keyword) is True :
            page_with_keyword.append(page)
        else: continue
    
    return page_with_keyword

new_page_list = keyword_page_list(file_names, 'Mark')
display(new_page_list)

#set the pages that do not hava the target keyword

original_list = file_names
elements_to_subtract = new_page_list

pages_without_keyword = [x for x in original_list if x not in elements_to_subtract]
display(pages_without_keyword)

#run face detection with OpenCV

def face_detect(file, scale):
    '''Pass in a file and scale factor, return image with faces detected'''
    
    cv_img = cv.imread(file)
    gray = cv.cvtColor(cv_img, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scale)
        
    return faces

#display(face_detect('a-0.png', 2))

#generate face detection images

def face_detect_images(file, scale) :

    pil_img = Image.open(file)
    drawing = ImageDraw.Draw(pil_img)
    
    for x,y,w,h in face_detect(file, scale) :
        drawing.rectangle((x,y,x+w,y+h), outline="white")
        
    
    return display(pil_img)

#crop the faces from the pages and resizes the images to prep for contact sheet

def cropped_images(file, scale, size) :
    
    '''Takes a file, crop scale, image size. Returns a list of cropped  and resized PIL images'''
    
    page_img = Image.open(file)
    cropped_list = []
    
    for x,y,w,h in face_detect(file, scale) :
        cropped_list.append(page_img.crop((x,y,x+w,y+h)))

    cropped_list_resize = []    
    
    for crop_img in cropped_list :
        crop_img = crop_img.resize(size)
        cropped_list_resize.append(crop_img)
        
    return cropped_list_resize

# create a contact sheet that's 5x2

def aggregate_images(file, scale, size):
    '''Aggregates all the cropped images onto a contact sheet'''
    
    images = cropped_images(file, scale, size)

    first_image = images[0]
    contact_sheet = PIL.Image.new(first_image.mode, (first_image.width*5,first_image.height*2))
    x = 0
    y = 0

    for img in images:
        # Lets paste the current image into the contact sheet
        contact_sheet.paste(img, (x, y) )
        # Now we update our X position. If it is going to be the width of the image, then we set it to 0
        # and update Y as well to point to the next "line" of the contact sheet.
        if x + first_image.width == contact_sheet.width:
            x = 0
            y = y + first_image.height
        else:
            x = x + first_image.width

    # resize and display the contact sheet
    contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
    
    return contact_sheet

#for page in pages_with_keyword

#final contact sheet if keyword was found 
#if keyword and image are found then below, else print keyword but not contact sheet

#if keyword is found, run this function

for page in ['a-0.png', 'a-1.png', 'a-2.png', 'a-3.png'] :
    
    try :

        file_name = page
        face_height = 200
        face_width = 200

        agg_img = aggregate_images(file_name, 2.11, (face_height, face_width))
        new_image = Image.new('RGB', (face_width*5, face_height + 25), color=(255, 255, 255))
        new_image.paste(agg_img, (0,25))

        draw = ImageDraw.Draw(new_image)
        text = "Results found in file {}".format(file_name)
        font = ImageFont.truetype("readonly/fanwood-webfont.ttf", size=20)
        draw.text((0,0), text, fill=(0,0,0), font=font)

        display(new_image)

    except :

        file_name1 = page
        new_image1 = Image.new('RGB', (face_width*5, 40), color=(255, 255, 255))
        draw1 = ImageDraw.Draw(new_image1)
        text1 = "Results found in file {}\nBut there were no faces in that file!".format(file_name1)
        font1 = ImageFont.truetype("readonly/fanwood-webfont.ttf", size=20)
        draw1.text((0,0), text1, fill=(0,0,0), font=font1)

        display(new_image1)

#final contact sheet if keyword was found 
#if keyword and image are found then below, else print keyword but not contact sheet

#if keyword is found, run this function

for page in new_page_list :
    
    try :

        file_name = page
        face_height = 200
        face_width = 200

        agg_img = aggregate_images(file_name, 2.11, (face_height, face_width))
        new_image = Image.new('RGB', (face_width*5, face_height + 25), color=(255, 255, 255))
        new_image.paste(agg_img, (0,25))

        draw = ImageDraw.Draw(new_image)
        text = "Results found in file {}".format(file_name)
        font = ImageFont.truetype("readonly/fanwood-webfont.ttf", size=20)
        draw.text((0,0), text, fill=(0,0,0), font=font)

        display(new_image)

    except :

        file_name1 = page
        new_image1 = Image.new('RGB', (face_width*5, 40), color=(255, 255, 255))
        draw1 = ImageDraw.Draw(new_image1)
        text1 = "Results found in file {}\nBut there were no faces in that file!".format(file_name1)
        font1 = ImageFont.truetype("readonly/fanwood-webfont.ttf", size=20)
        draw1.text((0,0), text1, fill=(0,0,0), font=font1)

        display(new_image1)
