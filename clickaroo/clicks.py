import time
import threading
from pynput.mouse import Button, Controller as Mouse
from pynput.keyboard import GlobalHotKeys, Controller as Keyboard


class Clickaroo(threading.Thread):

	def __init__(self):
		super().__init__()

		self.mouse = Mouse()
		self.delay = 0.001
		self.button = Button.left
		self.running = False
		self.program_running = True

		self.listener = GlobalHotKeys({
			'<ctrl>+<alt>+p': self.toggle_pause,
			'<ctrl>+<alt>+q': self.exit_out,
			'<ctrl>+<alt>+t': self.taps,
		})
		self.listener.start()

		self.keyboard = Keyboard()

	def mouse_move_click(self, x: int, y: int, click: bool = False):
		"""takes in absolute coords based on monitor resolution"""

		self.mouse_move(x, y)
		if click:
			self.mouse_one_click()

	def taps(self, keys='') -> None:
		if not keys:
			self.keyboard.type('12345')
		else:
			self.keyboard.type(keys)
		time.sleep(.1)

	def mouse_one_click(self):
		if self.running:
			self.running = False
		self.mouse.click(self.button)
		time.sleep(.05)

	def start_clicking(self) -> None:
		self.running = True

	def stop_clicking(self) -> None:
		self.running = False

	def exit(self) -> None:
		self.stop_clicking()
		self.program_running = False
		quit()
		exit()

	# the click loop will run for 5 seconds unless stopped early.
	def run(self) -> None:
		# I'm using pynput, so I can interrupt my clicks without having to kill xdotool
		while self.program_running:
			end_time = time.time() + 5
			while self.running:
				if time.time() >= end_time:
					self.running = False
				self.mouse.click(self.button)
				time.sleep(.05)
			time.sleep(.01)

	def mouse_move(self, x, y) -> None:
		# mouse.move is relative mouse.position is absoute.
		self.mouse.position = (int(x), int(y))

	def toggle_pause(self) -> None:
		# currently starts and stops clicking, but the clicker command will move once there is automation
		if not self.running:
			self.running = True
			self.start_clicking()
			# this will resume an action queue
		else:
			self.running = False
			self.stop_clicking()
			# pausing all other actions to be added later

	def exit_out(self) -> None:
		self.exit()


if __name__ == '__main__':

	clickaroni = Clickaroo()
	clickaroni.start()