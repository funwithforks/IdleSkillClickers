import cv2
from PIL import ImageGrab
from typing import Union


def screenshot(x1: int, x2: int, y2: int, y1: int) -> Union[ImageGrab.grab, None]:
	idle_screenshot = ImageGrab.grab(
		bbox=[x1, x2, y1, y2]
	)
	idle_screenshot.save('tmp2.png', 'png')
	if idle_screenshot:
		return idle_screenshot


if __name__ == "__main__":
	screenshot(100, 150, 200, 250)

