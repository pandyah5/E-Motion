import cv2
import numpy as np
import math
import time
import ctypes
from selenium import webdriver
import urllib.request # For python 2 just import urllib, urllib.request is needed for python 3+ because it has been been segmented into many subsets
from selenium.webdriver.common.keys import Keys # Helps to stimulate keyboard key presses
import os
import time

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location = "/usr/bin/chromium"


SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

time.sleep(1)

import speech_recognition as sr

import pyttsx3
converter = pyttsx3.init()
converter.setProperty('rate', 190)
converter.setProperty('volume', 10)

r = sr.Recognizer()
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
converter.setProperty('voice', voice_id) 
converter.say("Hi!, I am Julia. I handle this program's execution")
converter.say("Camera is deployed, all systems are functioning. Please select a mode")
converter.runAndWait()

mode = "none"

with sr.Microphone() as source:
    print("Speak Anything :")
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You said : {}".format(text))
    except:
        print("Sorry could not recognize what you said")
        mode = "none"
if "Alexa" in format(text):
    converter.say("Excuse me, I am Julia. Why don't you go and ask Alexa.")
    converter.runAndWait()
    mode = "none"
elif "Siri" in format(text):
    converter.say("Excuse me, I am Julia. Why don't you go and ask Siri.")
    converter.runAndWait()
    mode = "none"
elif "Cortana" in format(text):
    converter.say("Excuse me, I am Julia. Why don't you go and ask Cortana.")
    converter.runAndWait()
    mode = "none"
elif "game" in format(text) or "gaming" in format(text):
    converter.say("Selected gaming mode")
    converter.runAndWait()
    mode = "game"
elif "music" in format(text):
    converter.say("Selected music mode")
    converter.runAndWait()
    mode = "music"
elif "read" in format(text):
    converter.say("Selected study mode")
    converter.runAndWait()
    mode = "read"
elif "study" in format(text):
    converter.say("Selected study mode")
    converter.runAndWait()
    mode = "read"
    
if (mode == "game"):
    cap = cv2.VideoCapture(0)
    direct = "CENTER"
    while(1):

        # Take each frame
        _, frame = cap.read()

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        width = cap.get(3)
        height = cap.get(4)

        lower_red = np.array([158,59,153])
        upper_red = np.array([179,107,208])

        lower_green = np.array([65,116,117])
        upper_green = np.array([179,255,255])

        lower_yellow = np.array([33,32,213])
        upper_yellow = np.array([91,87,255])

        lower_blue = np.array([111,103,89])
        upper_blue = np.array([114,255,255])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_red, upper_red)
        mask1 = cv2.inRange(hsv, lower_green, upper_green)
        mask2 = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask3 = cv2.inRange(hsv, lower_blue, upper_blue)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'Asphalt 9: '+ direct,(0,50), font, 1, (99,74,154), 3, cv2.LINE_AA)

        try:
            # Green
            contours,hierarchy= cv2.findContours(mask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnt = max(contours, key = lambda x: cv2.contourArea(x))
            boxes = []
            for c in cnt:
                (x, y, w, h) = cv2.boundingRect(c)
                boxes.append([x,y, x+w,y+h])

            boxes = np.asarray(boxes)

            left = np.min(boxes[:,0])
            top = np.min(boxes[:,1])
            right = np.max(boxes[:,2])
            bottom = np.max(boxes[:,3])
            cv2.rectangle(frame, (left,top), (right,bottom), (0, 255, 0), 2)

            green_center_x = (left + right)/2
            green_center_y = (top + bottom)/2

            # Red
            cont,hier= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cntr = max(cont, key = lambda x: cv2.contourArea(x))

            box_red = []
            for c in cntr:
                (x, y, w, h) = cv2.boundingRect(c)
                box_red.append([x,y, x+w,y+h])

            box_red = np.asarray(box_red)

            left = np.min(box_red[:,0])
            top = np.min(box_red[:,1])
            right = np.max(box_red[:,2])
            bottom = np.max(box_red[:,3])
            cv2.rectangle(frame, (left,top), (right,bottom), (0, 0, 255), 2)

            red_center_x = (left + right)/2
            red_center_y = (top + bottom)/2

            try:
                ## Yellow
                cont_y,hier_y= cv2.findContours(mask2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                cntr_y = max(cont_y, key = lambda x: cv2.contourArea(x))
                area_yellow = cv2.contourArea(cntr_y)

                box_yellow = []
                for c in cntr_y:
                    (x, y, w, h) = cv2.boundingRect(c)
                    box_yellow.append([x,y, x+w,y+h])

                box_yellow = np.asarray(box_yellow)

                left = np.min(box_yellow[:,0])
                top = np.min(box_yellow[:,1])
                right = np.max(box_yellow[:,2])
                bottom = np.max(box_yellow[:,3])
                cv2.rectangle(frame, (left,top), (right,bottom), (0, 255, 255), 2)

                ## Blue
                cont_b,hier_b= cv2.findContours(mask3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                cntr_b = max(cont_b, key = lambda x: cv2.contourArea(x))
                area_blue = cv2.contourArea(cntr_b)

                box_blue = []
                for c in cntr_b:
                    (x, y, w, h) = cv2.boundingRect(c)
                    box_blue.append([x,y, x+w,y+h])

                box_blue = np.asarray(box_blue)

                left = np.min(box_blue[:,0])
                top = np.min(box_blue[:,1])
                right = np.max(box_blue[:,2])
                bottom = np.max(box_blue[:,3])
                cv2.rectangle(frame, (left,top), (right,bottom), (255, 0, 0), 2)

            except:
                pass

            ## Making decisions

            if (red_center_x * 1.1 < green_center_x):
                if (green_center_x > 1.25 * red_center_x):
                    PressKey(0x4B)
                    time.sleep(0.05)
                    ReleaseKey(0x4B)
                    direct = "EX_LEFT"
                else:
                    PressKey(0x4B)
                    time.sleep(0.03)
                    ReleaseKey(0x4B)
                    direct = "LEFT"

            elif (red_center_x > 1.1 * green_center_x):
                if (red_center_x > 1.25 * green_center_x):
                    PressKey(0x4D)
                    time.sleep(0.05)
                    ReleaseKey(0x4D)
                    direct = "EX_RIGHT"
                else:
                    PressKey(0x4D)
                    time.sleep(0.03)
                    ReleaseKey(0x4D)
                    direct = "RIGHT"

            else:
                direct = "CENTER"

            if (area_yellow > 100 and area_blue < 150):
                PressKey(0x39)
                time.sleep(0.05)
                ReleaseKey(0x39)
                PressKey(0x39)
                time.sleep(0.05)
                ReleaseKey(0x39)
                direct = "BOOST! Woaaah"

            if (area_blue > 150 and area_yellow > 100):
                PressKey(0x1C)
                time.sleep(0.05)
                ReleaseKey(0x1C)
                direct = "ENTER"

        except:
            pass


        cv2.imshow('frame',frame)
        cv2.imshow('green mask',mask1)
        cv2.imshow('red mask',mask)
        m = cv2.waitKey(5) & 0xFF
    #     k = cv2.waitKey(5) & 0xFF

    #     if k == 27: # Exit condition
    #         break

    cv2.destroyAllWindows()
    cap.release()
    
elif (mode == "music"):
    converter.say("Which music would you like to hear")
    converter.runAndWait()
    with sr.Microphone() as source:
        print("Song name :")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said : {}".format(text))
            driver = webdriver.Chrome("D:\Python files\Web Automation\chromedriver.exe")
            driver.get('https://www.youtube.com/') # Put the URL you wanna go to
            song_name = driver.find_element_by_id("search")
            song_name.send_keys(text)
            song_name.send_keys(Keys.ENTER)
            time.sleep(1)
            video = driver.find_elements_by_tag_name("ytd-video-renderer")
            (video[0]).click()

            ## Controls

            cap = cv2.VideoCapture(0)
            direct = "PLAYING"
            while(1):
                # Take each frame
                _, frame = cap.read()

                # Convert BGR to HSV
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                width = cap.get(3)
                height = cap.get(4)

                lower_red = np.array([97,93,139])
                upper_red = np.array([139,233,255])

                # Threshold the HSV image to get only blue colors
                mask = cv2.inRange(hsv, lower_red, upper_red)

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,'Music: '+ direct,(0,50), font, 1, (99,74,154), 3, cv2.LINE_AA)

                try:
                    contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    cnt = max(contours, key = lambda x: cv2.contourArea(x))

                    areacnt = cv2.contourArea(cnt)

                    boxes = []
                    for c in cnt:
                        (x, y, w, h) = cv2.boundingRect(c)
                        boxes.append([x,y, x+w,y+h])

                    boxes = np.asarray(boxes)

                    left = np.min(boxes[:,0])
                    top = np.min(boxes[:,1])
                    right = np.max(boxes[:,2])
                    bottom = np.max(boxes[:,3])
                    cv2.rectangle(frame, (left,top), (right,bottom), (255, 0, 0), 2)

                    if (areacnt > 2000):
                        if ((left + right)/2 > 2*width/3):
                            PressKey(0x2A)
                            PressKey(0x31)
                            time.sleep(0.05)
                            ReleaseKey(0x31)
                            ReleaseKey(0x2A)
                            direct = "NEXT VIDEO"
                            time.sleep(1)


                        elif ((left + right)/2 < width/3):
                            PressKey(0x39)
                            time.sleep(0.05)
                            ReleaseKey(0x39)
                            direct = "PAUSE"
                            time.sleep(1)

                        elif ((top + bottom)/2 > 2*height/3):
                            PressKey(0xC8)
                            time.sleep(0.05)
                            ReleaseKey(0xC8)
                            direct = "VOLUME UP"
                            time.sleep(0.5)

                        elif ((top + bottom)/2 < height/3):
                            PressKey(0xD0)
                            time.sleep(0.05)
                            ReleaseKey(0xD0)
                            direct = "VOLUME DOWN"
                            time.sleep(0.5)
                        else:
                            direct = "PLAYING"

                except:
                    pass


                cv2.imshow('frame',frame)

                m = cv2.waitKey(5) & 0xFF

            cv2.destroyAllWindows()
            cap.release()           
        except:
            print("Sorry could not recognize what you said")
            mode = "none"
            
elif (mode == "read"):
    try:
        ## Controls
        cap = cv2.VideoCapture(0)
        direct = "READING"
        while(1):
            # Take each frame
            _, frame = cap.read()

            # Convert BGR to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            width = cap.get(3)
            height = cap.get(4)

            lower_red = np.array([97,93,139])
            upper_red = np.array([139,233,255])

            # Threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv, lower_red, upper_red)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'READING: '+ direct,(0,50), font, 1, (99,74,154), 3, cv2.LINE_AA)

            try:
                contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                cnt = max(contours, key = lambda x: cv2.contourArea(x))

                areacnt = cv2.contourArea(cnt)

                boxes = []
                for c in cnt:
                    (x, y, w, h) = cv2.boundingRect(c)
                    boxes.append([x,y, x+w,y+h])

                boxes = np.asarray(boxes)

                left = np.min(boxes[:,0])
                top = np.min(boxes[:,1])
                right = np.max(boxes[:,2])
                bottom = np.max(boxes[:,3])
                cv2.rectangle(frame, (left,top), (right,bottom), (255, 0, 0), 2)

                if (areacnt > 2000):
                    if ((left + right)/2 < width/3):
                        PressKey(0x1D)
                        PressKey(0x4E)
                        time.sleep(0.05)
                        ReleaseKey(0x1D)
                        ReleaseKey(0x4E)
                        direct = "ZOOM IN"
                        time.sleep(1)


                    elif ((left + right)/2 > 2*width/3):
                        PressKey(0x1D)
                        PressKey(0x4A)
                        time.sleep(0.05)
                        ReleaseKey(0x1D)
                        ReleaseKey(0x4A)
                        direct = "ZOOM OUT"
                        time.sleep(1)

                    elif ((top + bottom)/2 > 2*height/3):
                        PressKey(0xC8)
                        time.sleep(0.3)
                        ReleaseKey(0xC8)
                        direct = "SCROLL UP"
                        time.sleep(0.1)

                    elif ((top + bottom)/2 < height/3):
                        PressKey(0xD0)
                        time.sleep(0.3)
                        ReleaseKey(0xD0)
                        direct = "SCROLL DOWN"  
                        time.sleep(0.1)
                    else:
                        direct = "READING"

            except:
                pass


            cv2.imshow('frame',frame)

            m = cv2.waitKey(5) & 0xFF

        cv2.destroyAllWindows()
        cap.release()           
    except:
        mode = "none"