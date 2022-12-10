from clickaroo.clicks import Clickaroo


if __name__ == '__main__':
	# basic clicks and single click thread
	# Can also press ctrl+alt+p to pause
	#                ctrl+alt+q to quit
	clickaroni = Clickaroo()
	print(clickaroni.click_thread.running)
	print(clickaroni.click_thread.program_running)
