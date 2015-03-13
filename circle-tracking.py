# import the necessary packages
import urllib
import numpy as np
import cv2
import httplib

#function of http commands to IP-camera
def action(what):
    httpServ = httplib.HTTPConnection("192.168.1.64", 8001)
    httpServ.connect()
    httpServ.request('GET', "/ptzctrl?username=admin&userpwd=admin&act=" + what)
	

while (True):
    #take frame from IP-camera, convert it to numpy array and transorm it to grayscale
    im = urllib.urlopen('http://192.168.1.64:8001/snapshot.jpg?username=admin&userpwd=admin')
    img = np.asarray(bytearray(im.read()), dtype=np.uint8)
    image = cv2.imdecode(img,0)

    # detect circles in the image
    circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 300)

    # ensure at least one circle was found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circle
        for (x, y, r) in circles:
            # corresponding to the center of the circle
            cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        # change the position of the IP-camera if needed
        if (x > 320 and x < 380 and y > 255 and y < 330):
            action('stop')

        if (x <= 320):
            action('left')
        elif (x >= 380):
            action('right')  

        if (y <= 255):    
            action('down')
        elif (y >= 330):
            action('up')

        action('stop')
	
