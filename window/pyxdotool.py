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
		"""This will hold and update data about the idle skilling window"""

	def search(self) -> Union[str, None]:
		"""pyxdotool.Window.search runs 'xdotool search --name <str>' to find
		idle skilling"""
		#isid = popen('xdotool search --name "^Idle Skilling$"')
		tempid = popen('xdotool search --name "pyxdotool"').read()
		if type(tempid) == str and len(tempid) > 1:
			# return isid
			return tempid.strip()

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
			'Position': [line1.group(1), line1.group(2)],
			'Screen': line1.group(3),
			'Geometry': [line2.group(1), line2.group(2)]
		}

		return data

	def mousemove(self, x, y) -> None:
		"""xdotool mousemove x y"""
		popen('xdotool mousemove ' + x + ' ' + y)

	def one_click(self) -> None:
		"""xdotool click 1"""
		popen('xdotool click 1')


if __name__ == '__main__':
	dork = Window()
	print('after print')
	print('pid')
	print(dork.pid)
	print('window id')
	print(dork.windowid)
	print('window geometry')
	print(dork.getwindowgeometry())
	print('focus window')
	dork.focus_idle_skilling()
	print('mouse move')
	# dork.mousemove(dork.getwindowgeometry().get('Geometry')[0], dork.getwindowgeometry().get('Geometry')[1])
	# test - move mouse to halfway in and halfway down the desired window. Much Success.
	dork.mousemove(
		str(int(dork.getwindowgeometry().get('Position')[0]) + int(int(dork.getwindowgeometry().get('Geometry')[0]) / 2)),
		str(int(dork.getwindowgeometry().get('Position')[1]) + int(int(dork.getwindowgeometry().get('Geometry')[1]) / 2)))
