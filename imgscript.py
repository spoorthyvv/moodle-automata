import os
import cv2

for image in os.listdir('preetham'):
	im = cv2.imread( 'preetham' + os.path.sep + image)
	gray =  cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	cv2.imwrite( 'black' + os.path.sep + image, gray)
