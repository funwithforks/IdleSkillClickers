from os import system, popen
from typing import Union, Optional, Dict, List, Any
import re


# this file is for handling window operations in linux

class Window:
	"""This class will handle window data using xdotool"""
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
		else:
			# Idle Skilling not found
			return None

	def getactivewindow(self) -> Union[str, None]:
		"""pyxdotool.Window.getactivewindow runs 'xdotool getactivewindow getwindowpid'
		to find the pid of idle skilling"""
		pid = popen('xdotool getactivewindow getwindowpid').read()
		if type(pid) == str and len(pid) > 1:
			return pid.strip()
		else:
			return None

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
dork.mousemove(dork.getwindowgeometry().get('Geometry')[0], dork.getwindowgeometry().get('Geometry')[1])
