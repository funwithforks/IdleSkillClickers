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
	# result = cv.matchTemplate(image, template, cv.TM_CCORR_NORMED, None, template)

	test = False

	cv.imwrite('bgbw.png', backgroung_cv)
	cv.imwrite('imbw.png', image_cv)
	# w, h = image_cv.shape[::-1]   # color
	w, h = image_cv.shape           # greyscale
	loc = np.where(res >= 0.8)
	if test:
		result_img = cv.cvtColor(np.array(backgroung_cv), cv.COLOR_GRAY2BGR)
		for pt in zip(*loc[::-1]):
			cv.rectangle(result_img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

			cv.imwrite('colorrec.png', result_img)
			cv.imwrite('result.png', backgroung_cv)

	return (res >= 0.7).any()


if __name__ == "__main__":
	# scrnsht = screenshot(10, 150, 200, 250)
	# scrnsht.save('tmp2.png', 'png')
	scrnsht = cv.imread('./images/train_button.png')
	backgrd = screenshot(1600, 824, (1600 + 960), (824 + 572))
	tmp = ImageGrab.grab()
	print(image_find(backgrd, scrnsht))
