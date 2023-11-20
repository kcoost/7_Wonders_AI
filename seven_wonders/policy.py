from sys import stdin

class Policy:
	def __init__(self):
		pass

	def make_choice(self, options):
		pass


class StupidAI(Policy):
	def make_choice(self, options):
		return 0

class Human(Policy):
	def make_choice(self, options):
		return int(stdin.readline())

