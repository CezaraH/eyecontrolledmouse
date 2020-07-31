"""CEZARA HULBER / ch5539w / 000920227
Eye Controlled Mouse for investigating Low-Cost Assistive Technologies
BSc. Digital Media Technologies
University of Greenwich
Class of 2019"""

import cv2
import time 
import Tkinter as tk
from PIL import Image, ImageTk
import win32api
import sys

#   This project imports the following open-source libraries:

#   OpenCV is a library of functions for computer vision. It enables the script to analyse camera
#   feed and discover contours that may resemble the eye pupil.

#   NumPy is a Python library for mathematical functions. It enables selecting the values for the
#   pupillometer (region of interest) that will be analysed by OpenCV.

#   time is a Python module for handling time-related tasks. In this project, it is used for debugging
#   purposes and ensuring that the camera loops are working.

#   Tkinter is a module that provides attributes and methods for windowed apps and enables multiple
#   GUI widget implementations.

#   PIL (Python Imaging Library) is a Python library that adds support for opening, manipulating,
#   and saving different image file formats. In this project, it is used to capture the feed from
#   the camera and creating a widget for it.

#   win32api is a module enabling various Windows 32 methods. It is the method used to transform the
#   OpenCV analysis into cursor movement.

#   sys is a module that provides access to system-specific parametres and functions.



window = tk.Tk()  # Creates window
window.title("Eye Controlled Mouse GUI")   # Window title
window.geometry("800x500")   # Window size


cap = cv2.VideoCapture(0)   # Type of Capture:  
cap2 = cv2.VideoCapture(1)  # 0 = default camera
                            # 1 = 2nd connected camera

                            
cam = tk.Label()            # The webcam widget
cam.pack()                  # Pack() places the widget in the window
cam2 = tk.Label()
cam2.pack()

trackbar_value = "Value"    # Trackbar global values to be references in the
window_name = "Calibration"      # calibration trackbar.


def first_camera():         # Default camera function

    # CV2 camera parametres - size, orientation (flip vertically for camera accuracy), shape

    _, frame = cap.read()
    pupillometer = frame[150: 350, 250: 450]
    pupillometer = cv2.flip(frame[150:350, 250:450], 1)     # vertically flips frame
    rows, cols, _ = pupillometer.shape
    thresh_val = cv2.getTrackbarPos(trackbar_value,
                                    window_name)

    """Converts camera capture to grey for faster performance."""
    gray_img = cv2.cvtColor(pupillometer, cv2.COLOR_BGR2GRAY)

    """Thresholding is a method which processes if the pixel value is greater than the threshold
    value and assigns it a new value. In this project, thresholding is used to process an image
    and assign each value as either black or white if they exceed or are below the threshold
    value which is by default 20, but can be increased or decreased using the calibration trackbar.

    The method processes the converted grey image and inverts the binary (black & white to white &
    black) thus the points of interest are represented by white in the thresholding window."""
    _, threshold = cv2.threshold(gray_img, thresh_val, 255, cv2.THRESH_BINARY_INV)

    """Contours find points with the same colour and intensity and connects them, being a common tool
    in developing object detection software. When multiple shapes are detected inside one another, a
    hierarchy is created. The countours hierarchy value below ensures that if multiple shapes are
    detected, the entire hierarchy is displayed using the RETR_TREE retrieval mode. CHAIN_APPROX_SIMPLE
    is a contour approximation method that removes unnecessary points when searching for contours."""
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    """Code reference: Sergio Canu (2019)."""
    contours = sorted(contours,
                      key=lambda x: cv2.contourArea(x),
                      reverse=True)
    """Code reference: Sergio Canu (2019)"""
    """This loop draws the contours and finds the centre point, drawing a vertical and a horizontal
    line to track the contour movement. The movement of the contours is assigned to the mouse cursor.
    Values have been multiplied for the cursor position to cover a bigger area of the screen."""
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)    # Creates a rectangle around the contours
        
        win32api.SetCursorPos((x*6+w*6,y*6+h*6))    # Cursor position value takes the value of the
                                                    # contours parametres
        """Code reference: Sergio Canu (2019)"""
        cv2.drawContours(pupillometer, [cnt], -7, (0, 0, 255), 7)
        cv2.rectangle(pupillometer, (x, y), (x + w, y + h), (255, 0, 0), 1)
        cv2.line(pupillometer, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 2)
        cv2.line(pupillometer, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2)
        break 

    """Using PIL, the camera feed is displayed as a Tkinter widget. Otherwise, the camera feed
    would be displayed in an external window, separate from the GUI."""
    img = Image.fromarray(pupillometer)
    imgtk = ImageTk.PhotoImage(image=img)
    cam.imgtk = imgtk
    cam.configure(image=imgtk)
    cam.after(10, first_camera)

    cv2.imshow(window_name,threshold)   # Displays the thresholding window and trackbar.


def show_trackbar():

    #   This function creates a trackbar in the thresholding window that allows the user to change
    #   the thresholding value for better calibration. 20 is the default value, 70 is the max.
    
    cv2.namedWindow(window_name)
    cv2.createTrackbar(trackbar_value, window_name, 20, 70, first_camera)


def second_camera():
    _, frame = cap2.read()
    pupillometer = frame[150: 350, 250: 450]
    pupillometer = cv2.flip(frame[150:350, 250:450], 1)
    rows, cols, _ = pupillometer.shape
    thresh_val = cv2.getTrackbarPos(trackbar_value, window_name)
    gray_img = cv2.cvtColor(pupillometer, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray_img, thresh_val, 255, cv2.THRESH_BINARY_INV)    
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)    # Creates a rectangle around the contours
        
        win32api.SetCursorPos((x*6+w*6,y*6+h*6))    # Cursor position value takes the value of the
                                                    # contours parametres

        cv2.drawContours(pupillometer, [cnt], -3, (255, 0, 0), 7)
        cv2.rectangle(pupillometer, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.line(pupillometer, (x + int(w/2), 0), (x + int(w/2), rows), (255, 255, 0), 2)
        cv2.line(pupillometer, (0, y + int(h/2)), (cols, y + int(h/2)), (255, 255, 0), 2)
        break

    img = Image.fromarray(pupillometer)
    imgtk = ImageTk.PhotoImage(image=img)
    cam2.imgtk = imgtk
    cam2.configure(image=imgtk)
    cam2.after(10, second_camera)

    cv2.imshow("threshold",threshold)   # Displays the thresholding window and trackbar.

def quit():
    sys.exit()

#   Button settings.

showtrackbar = tk.Button(window,text="Calibration settings",
                      bg="#84a6e0", fg="#fff",
                      activebackground="#5476af",
                      activeforeground="#84a6e0",
                      height=5, width=15,
                      font=("Helvetica", 15),
                      command=show_trackbar)
showtrackbar.pack(side=tk.LEFT, padx=20)


buttoncam = tk.Button(window,text="Turn on Camera 1",
                      bg="#84a6e0", fg="#fff",
                      activebackground="#5476af",
                      activeforeground="#84a6e0",
                      height=5, width=15,
                      font=("Helvetica", 15),
                      command=first_camera)
buttoncam.pack(side=tk.LEFT, padx=0)


buttonchange = tk.Button(window,text="Turn on Camera 2",
                      bg="#84a6e0", fg="#fff",
                      activebackground="#5476af",
                      activeforeground="#84a6e0",
                      height=5, width=15,
                      font=("Helvetica", 15),
                      command=second_camera)
buttonchange.pack(side=tk.LEFT, padx=20)


quitb = tk.Button(window,text="QUIT",
                      bg="#c12f2c", fg="#fff",
                      activebackground="#56100e",
                      activeforeground="#fff",
                      height=5, width=15,
                      font=("Helvetica", 15),
                      command=quit)
quitb.pack(side=tk.LEFT, padx=0)

window.mainloop() #Window's event loop that stays open, waiting to handle events until it is closed


