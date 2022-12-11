import time
import threading
from pynput.mouse import Button, Controller as Mouse
from pynput.keyboard import KeyCode, Key, GlobalHotKeys, Controller as Keyboard


class Tapper(threading.Thread):
	def __init__(self):
		super(Tapper, self).__init__()
		self.keyboard = Keyboard()

	def taps(self, keys='') -> None:
		if not keys:
			self.keyboard.type('12345')
		else:
			self.keyboard.type(keys)


# click class
class Clicker(threading.Thread):

	def __init__(self, delay, button):
		super(Clicker, self).__init__()
		self.mouse = Mouse()
		self.delay = delay
		self.button = button
		self.running = False
		self.program_running = True

	def mouse_click(self, clicks):
		click_count = 0
		while click_count < clicks:
			self.mouse.click(self.button)
			click_count += 1

	def start_clicking(self):
		self.running = True

	def stop_clicking(self):
		self.running = False

	def exit(self):
		self.stop_clicking()
		self.program_running = False

	# the click loop will run for 5 seconds unless stopped early.
	def run(self):
		# I'm using pynput, so I can interrupt my clicks without having to kill xdotool
		while self.program_running:
			end_time = time.time() + 5
			while self.running:
				if time.time() >= end_time:
					self.running = False
				self.mouse.click(self.button, 200)
				time.sleep(0.1)

	def mouse_move(self, x, y) -> None:
		# mouse.move is relative mouse.position is absoute.
		self.mouse.position = (x, y)


class InputMan:

	def __init__(self, owner):
		self.combination = {Key.ctrl, KeyCode(char='q')}
		self.listener = GlobalHotKeys({
			'<ctrl>+<alt>+p': self.toggle_pause,
			'<ctrl>+<alt>+q': self.exit_out,
			'<ctrl>+<alt>+t': self.taps,
		})
		self.listener.start()
		self.clickaroni = owner

	def taps(self) -> None:
		self.clickaroni.tapper_thread.taps()

	def toggle_pause(self):
		# currently starts and stops clicking, but the clicker command will move once there is automation
		if not self.clickaroni.click_thread.running:
			self.clickaroni.click_thread.running = True
			self.clickaroni.click_thread.start_clicking()
			# this will resume an action queue
		else:
			self.clickaroni.click_thread.running = False
			self.clickaroni.click_thread.stop_clicking()
			# pausing all other actions to be added later

	def exit_out(self):
		self.clickaroni.click_thread.exit()


class Clickaroo:

	def __init__(self):
		self.click_thread = Clicker(delay=0.001, button=Button.left)
		self.click_thread.start()

		self.tapper_thread = Tapper()
		self.tapper_thread.start()

		self.inputs = InputMan(self)


if __name__ == '__main__':

	clickaroni = Clickaroo()
