import threading
import datetime
import time
from queue import Queue
from threading import Thread
from clickaroo.clicks import Clickaroo
from window.pyxdotool import Window
from idleCV.idleCV import IdleCV
import tkinter as tk
from pynput.keyboard import GlobalHotKeys


class Action:
	def __init__(self):
		self.current_location: str = 'midas'
		self.next_location: str = ''
		self.midas_test_thread = Thread(target=self.midas, daemon=True)
		self.queue_dict: dict = {
			'midas': self.midas,
			'spelunker': self.spelunker,
			'strafe': self.strafe,
		}
		self.current_task: str = 'midas'
		self.previous_task: str = ''

		# clickaroni handles clicking, moving the mouse, and pressing keys.
		# It also listens for key combinations to control the application.
		self.clickaroni = Clickaroo()
		self.clickaroni.start()

		self.xdo = Window()
		self.tasklet = self.Tasklet(self)

		# card_stop is to stop looking for cards when True
		self.card_stop = False

		# OpenCV is in a thread. Currently just a card seeker/clicker.
		self.card_thread = threading.Thread(
			target=self.opencv_thread,
			daemon=True
		)
		self.card_thread.start()

		self.listener = GlobalHotKeys({
			'<ctrl>+<alt>+p': self.clickaroni.toggle_pause,
			'<ctrl>+<alt>+q': self.clickaroni.exit_out,
			'<ctrl>+<alt>+t': self.clickaroni.taps,
		})
		self.listener.start()

	def opencv_thread(self):
		if not self.card_stop:
			self.card_thread = threading.Thread(
				target=self.tasklet.card_clicker_thread(),
				daemon=True)
			self.card_thread.start()

	class Tasklet:
		def __init__(self, owner):
			self.action = owner
			self.idle_cv = IdleCV()
			self.card_list = []

		def card_clicker_thread(self):
			while True:
				if (self.action.current_location == 'midas' or self.action.current_location == 'fight') and \
					(self.action.clickaroni.program_running and not self.action.card_stop):
					backgrd = self.idle_cv.screenshot(1600, 824, (1600 + 960), (824 + 572))
					a = self.idle_cv.find_card(backgrd)
					if a:
						for card in a:
							# print(f'card: {card} in cards: {cards}')
							self.action.tasklet.card_mouse(x=card[0], y=card[1])
				time.sleep(0.5)

		def x_y_percent(self, x: int, y: int) -> list[int]:
			"""x_y_percent takes in an x and y coord and turns it into a percent coord for the game window."""
			# {'Position': ['1601', '824'], 'Screen': '0', 'Geometry': ['959', '572']}
			tmp = self.action.xdo.getwindowgeometry()
			gx = tmp.get('Geometry')[0]
			gy = tmp.get('Geometry')[1]
			return [int((x / gx) * 100), int((y / gy) * 100), tmp]

		def make_relative(self, percentx: int = None, percenty: int = None, values: list = None) -> list[str]:
			if values:
				tmp = values[2]
				percentx = values[0]
				percenty = values[1]
			else:
				tmp = self.action.xdo.getwindowgeometry()
			return [str(tmp.get('Position')[0] + int(tmp.get('Geometry')[0] / (100 / percentx))),
					str(tmp.get('Position')[1] + int(tmp.get('Geometry')[1] / (100 / percenty)))]

		def card_mouse(self, x: int, y: int) -> None:
			"""Same as rel_mouse_move but adds an x y percent calc"""
			# print(f'cardmouse x: {x}, y: {y}')
			self.action.clickaroni.mouse_move(*self.make_relative(values=self.x_y_percent(x, y)))
			self.action.clickaroni.mouse_one_click()

		def rel_mouse_move(self, percentx, percenty, click: bool) -> None:
			self.action.clickaroni.mouse_move(*self.make_relative(percentx, percenty))
			if click:
				self.action.clickaroni.mouse_one_click()

		def toggle_top_skill(self):
			top_toggle_percents = [25, 82]
			# self.xdo.rel_mouse_move(*top_toggle_percents, True) # xdotool version
			self.rel_mouse_move(*top_toggle_percents, True)     # pynput version
			time.sleep(.1)

		def toggle_bottom_skill(self):
			bottom_toggle_percents = [21, 94]
			self.rel_mouse_move(*bottom_toggle_percents, True)
			time.sleep(.1)

		def tap_strafe(self):
			strafe_percents = [41, 85]
			self.rel_mouse_move(*strafe_percents, True)
			time.sleep(.1)

		def toggle_mark(self, strafe: bool = False):
			self.toggle_bottom_skill()
			self.action.clickaroni.taps('1')
			if strafe:
				self.tap_strafe()
			self.toggle_top_skill()
			time.sleep(.1)

		def fight_effects_off(self):
			...

		def fight_loop(self, duration) -> None:
			self.toggle_top_skill()
			endtime = time.time() + duration
			while time.time() <= endtime:
				self.action.clickaroni.taps('12345')
				time.sleep(0.1)
				self.toggle_bottom_skill()
				self.toggle_bottom_skill()
				self.action.clickaroni.taps('12345')
				self.toggle_bottom_skill()
				self.toggle_top_skill()
				time.sleep(2.5)
			self.toggle_top_skill()

	def interrupt_me(self, func=None, funcy=None) -> None:
		# this function will be a thread that will run the task. It will be terminated
		# when pause key pressed.
		if func:
			self.queue_dict.get(func)()
		if funcy:
			funcy()

	def midas(self) -> None:
		# currently assuming it's ready for midas...
		# currently 40 seconds from midas start to midas ready.
		midas = [50, 60]
		self.current_location = 'midas'
		print('doing midas click routine')
		self.tasklet.toggle_mark()
		self.clickaroni.taps('3')
		time.sleep(.1)
		print('clicking', end='')
		self.tasklet.rel_mouse_move(*midas, True)
		self.clickaroni.start_clicking()
		time.sleep(5.25)
		print('\rremoving mark', end='')
		self.tasklet.toggle_mark(strafe=True)
		if self.previous_task == 'midas' or self.previous_task == '':
			print('\rfight loop for 35 more seconds...', end='')
			self.tasklet.fight_loop(35.3)
		print('\rdone\n')

	def spelunker(self) -> None:
		self.current_location = 'spelunker'
		print(f"you are in the spelunker area")
		time.sleep(.5)
		print('clicking extract')
		print('waiting for extract animation...')
		time.sleep(2)
		print('clicking bag')
		time.sleep(.2)
		print('jumping')
		time.sleep(.2)
		print('jump countdown started\n')

	def strafe(self):
		self.current_location = 'portal'
		count = 0
		while count < 2:
			print('mouse move to and click portal button')
			self.current_location = 'portal'
			time.sleep(1)
			print("mouse move to and click dude")
			time.sleep(.5)
			print('mouse move to and click tunnel button')
			self.current_location = 'tunnel'
			time.sleep(1)
			count += 1
		# setting task to midas since queue repeats last task if queue is empty
		self.current_task = 'midas'
		self.transitions(self.current_task)

	def transitions(self, destination):
		# I need to store a lot of click patterns in here.
		print(f'You are currently in {self.current_location} and going to {destination}...')
		time.sleep(.5)
		print("clicking through pages")
		time.sleep(1)
		print('you have arrived to where you are going\n')


class TestQueue:

	def __init__(self):
		self.q = Queue()
		self.time_dict: dict = {
			'midas': 0
		}
		self.start_time: datetime = datetime.time()
		self.actions = Action()

		# setting daemon to True allows program to stop when clicker receives the quit keys
		self.process = Thread(target=self.the_queue, daemon=True)
		self.process.start()
		# self.actions.card_mon.start()

		self.idle_skilling_running: bool = True if self.actions.xdo.search() else False

	def the_queue(self) -> None:
		time.sleep(1)
		while self.actions.clickaroni.program_running:
			print(f'search output: {self.actions.xdo.search()}')
			if not self.actions.xdo.search():
				time.sleep(1)
				print('Idle Skilling not running. Sleep 1 second...')
				continue
			self.countdown_timers()
			print(f'current task is {self.actions.current_task},\tprevious task is {self.actions.previous_task}')
			if self.q.empty():
				task = self.actions.current_task
			else:
				task = self.q.get()
				if self.actions.current_task != task:
					print(f'current task: {self.actions.current_task}, new task: {task}')
					self.actions.current_task = task
					self.actions.transitions(task)

			interrupt_task = Thread(target=self.actions.interrupt_me(func=task), daemon=True)
			interrupt_task.start()
			interrupt_task.join()

			self.actions.previous_task = task

			# sleep is for print testing
			time.sleep(2.1)

	def countdown_timers(self):
		#
		...

	def set_timer(self, timer):
		...

	def add_to_queue(self, something):
		self.q.put(something)


class IdleWindow:
	def __init__(self, idleroot: tk.Tk, the_data):
		self.idleroot = idleroot
		self.counter = 0
		self.data = the_data
		self.label = tk.Label(idleroot, text='Counter: 0')
		self.label.pack()
		self.update_label()

	def update_label(self):
		self.counter += 1
		self.label['text'] = f'Counter: {self.counter}'
		self.idleroot.after(1000, self.update_label)


if __name__ == '__main__':
	q = TestQueue()
	q.add_to_queue('midas')
	# root = tk.Tk()
