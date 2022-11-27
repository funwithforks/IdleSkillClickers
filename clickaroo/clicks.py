import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import KeyCode, Key, GlobalHotKeys


# click class
class Clicker(threading.Thread):

	def __init__(self, delay, button):
		super(Clicker, self).__init__()
		self.mouse = Controller()
		self.delay = delay
		self.button = button
		self.running = False
		self.program_running = True

	def mouse_click(self, clicks):
		click_count = 0
		while click_count < clicks:
			self.mouse.click(self.button)
			clicks -= 1

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
				self.mouse.click(self.button)
				time.sleep(0.001)

	def mouse_move(self, x, y) -> None:
		self.mouse.move(x, y)


class InputMan:

	def __init__(self, owner):
		self.combination = {Key.ctrl, KeyCode(char='q')}
		self.is_paused = False
		self.listener = GlobalHotKeys({
			'<ctrl>+<alt>+p': self.toggle_pause,
			'<ctrl>+<alt>+q': self.exit_out
		})
		self.listener.start()
		self.clickaroni = owner

	def toggle_pause(self):
		if not self.is_paused:
			self.is_paused = True
			self.clickaroni.click_thread.stop_clicking()
			# pausing all other actions to be added later
		else:
			self.is_paused = False
			# this will resume an action queue

	def exit_out(self):
		self.clickaroni.click_thread.exit()


class Clickaroo:

	def __init__(self):
		self.click_thread = Clicker(delay=0.001, button=Button.left)
		self.click_thread.start()

		self.inputs = InputMan(self)


if __name__ == '__main__':

	clickaroni = Clickaroo()
