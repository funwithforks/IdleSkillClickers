import cv2
from PIL import ImageGrab
from typing import Union


def screenshot(x1, x2, y2, y1) -> Union[ImageGrab, None]:
	tmp_screenshot = ImageGrab.grab()
	tmp2 = tmp_screenshot.crop((x1, x2, y1, y2))
	del tmp_screenshot
	tmp2.save('tmp2.png', 'png')

	if tmp2:
		return tmp2


if __name__ == "__main__":
	screenshot(100, 150, 200, 250)

