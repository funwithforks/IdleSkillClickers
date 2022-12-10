from multiprocessing import Queue
import datetime
import time
from threading import Thread
from clickaroo.clicks import Clickaroo


class TestAction:
	def __init__(self):
		self.current_location: str = 'midas'
		self.next_location: str = ''
		self.queue_dict: dict = {
			'midas': self.midas,
			'spelunker': self.spelunker,
			'strafe': self.strafe,
		}
		self.current_task: str = 'midas'

	def midas(self):
		self.current_location = 'midas'
		print('doing midas click routine')
		print('readying midas')
		time.sleep(1)
		print('clicking')
		time.sleep(5)
		print('removing mark')
		time.sleep(1)
		print('done\n')

	def spelunker(self):
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
		self.current_task = None
		self.actions = TestAction()
		self.clickaroni = Clickaroo()

		# setting daemon to True allows program to stop when clicker receives the quit keys
		self.process = Thread(target=self.the_queue, daemon=True)
		self.process.start()

	def the_queue(self) -> None:
		time.sleep(1)
		while True:
			if not self.clickaroni.click_thread.program_running:
				quit()
			self.countdown_timers()
			print(f'current task is {self.actions.current_task}')
			if self.q.empty():
				self.actions.queue_dict.get(self.actions.current_task)()
			else:
				task = self.q.get()
				if self.actions.current_task != task:
					print(f'current task: {self.actions.current_task}, new task: {task}')
					self.actions.current_task = task
					self.actions.transitions(task)
				self.actions.queue_dict.get(self.actions.current_task)()

			# sleep is for print testing
			time.sleep(2.1)

	def countdown_timers(self):
		#
		...

	def set_timer(self, timer):
		...

	def add_to_queue(self, something):
		print('asdf')
		self.q.put(something)


if __name__ == '__main__':
	q = TestQueue()
	# t = TestAction()
	# q.add_to_queue((print, 'hellodo'))
	q.add_to_queue('midas')
	q.add_to_queue('strafe')
	q.add_to_queue('spelunker')
	# q.the_queue()
	print('thread test')
