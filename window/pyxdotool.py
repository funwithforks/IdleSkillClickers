import time
from os import system, popen
from typing import Union, Any
import re


class Window:
	"""This class will handle window data using xdotool,
	I now realize I should not do this..."""
	def __init__(self):
		self.pid = self.getactivewindow()
		self.windowid = self.search()

	class IdleWindow:
		"""This will hold data about the idle skilling window"""

	def search(self) -> Union[str, None]:
		"""pyxdotool.Window.search runs 'xdotool search --name <str>' to find
		idle skilling"""
		isid = popen('xdotool search --name "^Idle Skilling$"').read()
		#tempid = popen('xdotool search --name "pyxdotool"').read()
		if type(isid) == str and len(isid) > 1:
			return isid.strip()

	def open_idle_skilling(self):
		popen('steam  steam://rungameid/1048370 &')

	def close_idle_skilling(self):
		popen('steam steam://rungameid/1048370 -shutdown &')

	def getactivewindow(self) -> Union[str, None]:
		"""pyxdotool.Window.getactivewindow runs 'xdotool getactivewindow getwindowpid'
		to find the pid of idle skilling"""
		pid = popen('xdotool getactivewindow getwindowpid').read()
		if type(pid) == str and len(pid) > 1:
			return pid.strip()

	def windowkill(self) -> None:
		"""Kills a window"""
		popen('xdotool windowtool ' + self.windowid)

	def dotype(self, text='12345') -> None:
		"""Types into a window without needing to focus"""
		popen('xdotool type --window ' + self.windowid + ' ' + text)

	def focus_idle_skilling(self) -> None:
		"""pyxdotool.Window.getactivewindow runs 'xdotool windowactivate <window id>
		to put Idle Skilling in the foreground"""
		system('xdotool windowactivate ' + str(self.windowid))

	def getwindowgeometry(self) -> dict[str, list[str | Any] | str | Any]:
		output = popen('xdotool getwindowgeometry ' + str(self.windowid)).read().splitlines()
		line1 = re.search("(\d+),(\d+)\s\(screen:\s(\d+)", output[1])
		line2 = re.search("(\d+)x(\d+)", output[2])
		data = {
			'Position': [int(line1.group(1)), int(line1.group(2))],
			'Screen': int(line1.group(3)),
			'Geometry': [int(line2.group(1)), int(line2.group(2))]
		}

		return data

	def mousemove(self, x, y) -> None:
		"""xdotool mousemove x y"""
		popen('xdotool mousemove ' + x + ' ' + y)

	def rel_mouse_move(self, percentx, percenty, click: bool = False) -> None:
		self.mousemove(*self.make_relative(percentx, percenty))
		if click:
			self.one_click()

	def one_click(self) -> None:
		"""xdotool click 1"""
		popen('xdotool click 1')

	def x_y_percent(self, x: int, y: int) -> list[int]:
		"""x_y_percent takes in an x and y coord and turns it into a percent coord for the game window."""
		# {'Position': ['1601', '824'], 'Screen': '0', 'Geometry': ['959', '572']}
		tmp = self.getwindowgeometry()
		gx = tmp.get('Geometry')[0]
		gy = tmp.get('Geometry')[1]
		return [int((x / gx) * 100), int((y / gy) * 100), tmp]

	def make_relative(self, percentx: int = None, percenty: int = None, values: list = None) -> list[str]:

		if values:
			tmp = values[2]
			percentx = values[0]
			percenty = values[1]
		else:
			tmp = self.getwindowgeometry()
		return [str(tmp.get('Position')[0] + int(tmp.get('Geometry')[0] / (100 / percentx))),
				str(tmp.get('Position')[1] + int(tmp.get('Geometry')[1] / (100 / percenty)))]

	def card_mouse(self, x:int, y:int) -> None:
		self.mousemove(*dork.make_relative(values=dork.x_y_percent(x, y)))


if __name__ == '__main__':
	dork = Window()
	print('after print')
	print('pid')
	print(dork.pid)
	print('window id')
	windowid = dork.windowid
	if windowid:
		print(dork.windowid)
	else:
		print('\t\tIdle Skilling not running. Expect an error...')
	print('window geometry')
	print(dork.getwindowgeometry())
	print('focus window')
	dork.focus_idle_skilling()
	print('mouse move')
	# dork.mousemove(dork.getwindowgeometry().get('Geometry')[0], dork.getwindowgeometry().get('Geometry')[1])
	# test - move mouse to halfway in and halfway down the desired window. Much Success.
	# dork.mousemove(*dork.make_relative(percentx=40, percenty=12))
	dork.card_mouse(100, 300)
