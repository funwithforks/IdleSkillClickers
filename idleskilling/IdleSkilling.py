from multiprocessing import Queue
import datetime
import time
from threading import Thread
from clickaroo.clicks import Clickaroo
from window.pyxdotool import Window


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

		self.clickaroni = Clickaroo()
		self.xdo = Window()
		self.tasklet = self.Tasklet(self)

	class Tasklet:
		def __init__(self, owner):
			self.action = owner

		def make_relative(self, percentx, percenty) -> list[int]:
			tmp = self.action.xdo.getwindowgeometry()
			return [int(tmp.get('Position')[0]) + int(int(tmp.get('Geometry')[0]) / (100 / percentx)),
					int(tmp.get('Position')[1]) + int(int(tmp.get('Geometry')[1]) / (100 / percenty))]

		def rel_mouse_move(self, percentx, percenty, click: bool) -> None:
			self.action.clickaroni.click_thread.mouse_move(*self.make_relative(percentx, percenty))
			if click:
				self.action.clickaroni.click_thread.mouse_click(1)

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
			self.action.clickaroni.tapper_thread.taps('1')
			if strafe:
				self.tap_strafe()
			self.toggle_top_skill()
			time.sleep(.1)

		def fight_loop(self, duration) -> None:
			self.toggle_top_skill()
			endtime = time.time() + duration
			while time.time() <= endtime:
				self.action.clickaroni.tapper_thread.taps('12345')
				time.sleep(3)
			self.toggle_top_skill()

	def interrupt_me(self, func) -> None:
		# this function will be a thread that will run the task. It will be terminated
		# when pause key pressed.
		self.queue_dict.get(func)()

	def midas(self) -> None:
		# currently assuming it's ready for midas...
		# currently 40 seconds from midas start to midas ready.
		midas = [50, 60]
		self.current_location = 'midas'
		print('doing midas click routine')
		self.tasklet.toggle_mark()
		self.clickaroni.tapper_thread.taps('3')
		time.sleep(.1)
		print('clicking', end='')
		self.tasklet.rel_mouse_move(*midas, True)
		self.clickaroni.inputs.start_clicking()
		time.sleep(5.25)
		print('\rremoving mark', end='')
		self.tasklet.toggle_mark(True)
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

	def the_queue(self) -> None:
		time.sleep(1)
		while True:
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

			self.interrupt_task = Thread(target=self.actions.interrupt_me(task), daemon=True)
			self.interrupt_task.start()
			self.interrupt_task.join()

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


if __name__ == '__main__':
	q = TestQueue()
	q.add_to_queue('midas')
	# q.add_to_queue('strafe')
	# q.add_to_queue('spelunker')
