import time

import cv2 as cv
from PIL import ImageGrab
from typing import Union
import numpy as np


def screenshot(x1: int, y1: int, x2: int, y2: int) -> Union[ImageGrab.grab, None]:
	"""PIL seems to be faster than pyautogui for screen grabs
	bbox coord [x_left, y_top, x_right, y_bottom]"""
	idle_screenshot = ImageGrab.grab(
		bbox=[x1, y1, x2, y2]
	)
	# idle_screenshot.save('file.png', 'png')
	if idle_screenshot:
		return idle_screenshot


def cropped_screenshot(image: ImageGrab.grab, l1, l2, h1, h2) -> ImageGrab.grab:
	"""cropped_screenshot will return a portion of the last capped frame, used to pass to image_find
	and reduce the search size"""
	return image[l1:l2, h1:h2]


def image_find(background, image):
	# different images will probably be better with color and some with greyscale
	# backgroung_cv = cv.cvtColor(np.array(background), cv.COLOR_RGB2BGR)
	# will look into masking to simplify all this.
	backgroung_cv = cv.cvtColor(np.array(background), cv.COLOR_BGR2GRAY)
	image_cv = cv.cvtColor(np.array(image), cv.COLOR_BGR2GRAY)

	res = cv.matchTemplate(backgroung_cv, image_cv, cv.TM_CCOEFF_NORMED)
	# following line requires I replace background of images with transparency and use it as
	#     both mask and template
	result = cv.matchTemplate(image, image_cv, cv.TM_CCORR_NORMED, None, image_cv)

	test = False

	cv.imwrite('bgbw.png', backgroung_cv)
	cv.imwrite('imbw.png', image_cv)
	# w, h = image_cv.shape[::-1]   # color
	w, h = image_cv.shape[::-1]           # greyscale
	loc = np.where(res >= 0.8)
	if test:
		result_img = cv.cvtColor(np.array(backgroung_cv), cv.COLOR_GRAY2BGR)
		for pt in zip(*loc[::-1]):
			# cv2.rectangle(image, start_point, end_point, color, thickness)
			cv.rectangle(result_img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

			cv.imwrite('colorrec.png', result_img)
			cv.imwrite('result.png', backgroung_cv)

	return (res >= 0.7).any()


def find_card(background) -> Union[list[list[int]], None]:
	"""find_card finds cards based on contours and returns the center point of each card in the frame.
	Overlapping cards will interfere with detection..."""
	# Convert the image to grayscale
	gray_bg = cv.cvtColor(np.array(background), cv.COLOR_BGR2GRAY)
	# Find the edges of the image using Canny edge detection
	edges = cv.Canny(gray_bg, 50, 100)
	# Find contours in the image
	contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

	coords = []

	for c in contours:
		rect = cv.minAreaRect(c)
		# dimensions of a card ((coords), (size), orientation)
		# ((407.0, 260.0), (61.99999237060547, 43.99999237060547), 90.0)
		if rect[2] != 90.0 \
				or not (61.8 < round(rect[1][0], 2) < 62.1) \
				or not (43.8 < round(rect[1][1], 2) < 44.1):
			continue
		# Get the bounding box coordinates of the rectangle
		box = cv.boxPoints(rect)
		# Convert the coordinates to integers
		box = np.int0(box)
		# get center coords of box for clicking
		box_center = [int(rect[0][0]), int(rect[0][1])]
		coords.append(box_center)

	if len(coords) > 0:
		return coords


def image_find_t(background, image):
	# image_find_t takes in a png with transparency in the background and uses it as the
	# mask and the template. So far it seems to work well at finding the image with any background.
	# Although I get false positives if I am below 0.91.
	# I suppose I could further crop the screenshot for each match to where the match should be.
	background_cv = cv.cvtColor(np.array(background), cv.TM_CCORR_NORMED)
	result = cv.matchTemplate(background_cv, image, cv.TM_CCORR_NORMED, None, image)
	# print(*image.shape)
	w, h = image.shape[1], image.shape[0]
	loc = np.where(result >= .8)

	# result_img = cv.cvtColor(np.array(background_cv), cv.TM_CCORR_NORMED) # 100% FP
	result_img = cv.cvtColor(np.array(background_cv), cv.TM_CCOEFF_NORMED)
	for pt in zip(*loc[::-1]):
		# cv2.rectangle(image, start_point, end_point, color, thickness)
		cv.rectangle(result_img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
		if (result >= 0.96).any():
			print('printed')
			cv.imwrite('colorrec1.png', result_img)
			cv.imwrite('result1.png', background_cv)

	return (result >= 0.96).any()


def card_loop():
	while True:
		scrnsht = cv.imread('./images/card_mask.png', cv.IMREAD_COLOR)
		backgrd = screenshot(1600, 824, (1600 + 960), (824 + 572))
		# image_find_t(backgrd, scrnsht)
		a = find_card(backgrd)
		if a:
			print(a)
		time.sleep(1)


if __name__ == "__main__":
	# scrnsht = screenshot(10, 150, 200, 250)
	# scrnsht.save('tmp2.png', 'png')
	card_loop()

