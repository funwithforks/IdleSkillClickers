import time
import threading
from pynput.mouse import Button, Controller as Mouse
from pynput.keyboard import KeyCode, Key, GlobalHotKeys, Controller as Keyboard
from queue import PriorityQueue


class Tapper(threading.Thread):
	def __init__(self):
		super(Tapper, self).__init__()
		self.keyboard = Keyboard()

	def taps(self, keys='') -> None:
		if not keys:
			self.keyboard.type('12345')
		else:
			self.keyboard.type(keys)
		time.sleep(.1)


# click class
class Clicker(threading.Thread):

	def __init__(self, delay, button):
		super(Clicker, self).__init__()
		self.mouse = Mouse()
		self.delay = delay
		self.button = button
		self.running = False
		self.program_running = True

	def mouse_click(self, clicks) -> None:
		click_count = 0
		while click_count < clicks:
			self.mouse.click(self.button)
			click_count += 1
			time.sleep(.02)

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
				time.sleep(.1)

	def mouse_move(self, x, y) -> None:
		# mouse.move is relative mouse.position is absoute.
		self.mouse.position = (int(x), int(y))


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

	def toggle_pause(self) -> None:
		# currently starts and stops clicking, but the clicker command will move once there is automation
		if not self.clickaroni.click_thread.running:
			self.clickaroni.click_thread.running = True
			self.clickaroni.click_thread.start_clicking()
			# this will resume an action queue
		else:
			self.clickaroni.click_thread.running = False
			self.clickaroni.click_thread.stop_clicking()
			# pausing all other actions to be added later

	def start_clicking(self) -> None:
		if not self.clickaroni.click_thread.running:
			self.clickaroni.click_thread.running = True
			self.clickaroni.click_thread.start_clicking()

	def exit_out(self) -> None:
		self.clickaroni.action.card_stop = True
		self.clickaroni.click_thread.exit()


class Clickaroo:

	def __init__(self, owner):
		self.action = owner

		self.click_thread = Clicker(delay=0.001, button=Button.left)
		self.click_thread.start()

		self.tapper_thread = Tapper()
		self.tapper_thread.start()

		self.inputs = InputMan(self)

		self.input_queue = PriorityQueue()

	def input_queue_handler(self):

		while True:
			if self.input_queue.empty():
				time.sleep(0.1)
			else:
				self.input_queue.get()
				time.sleep(0.1)

	@staticmethod
	def input_wrapper(func, *args):
		return func(*args)

	def input_queue_put(self, priority: int, func, *args):
		self.input_queue.put((priority, func, args))

	def mouse_move_click(self, x: int, y: int, click: bool = False):
		"""takes in absolute coords based on monitor resolution"""
		self.click_thread.mouse_move(x, y)
		if click:
			self.click_thread.mouse_click(1)

	def contribution_test(self):
		pass


if __name__ == '__main__':

	clickaroni = Clickaroo()
