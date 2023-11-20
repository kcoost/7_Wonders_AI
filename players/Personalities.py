from sys import stdin
from common import *
import cards


class Personality:
	def __init__(self):
		pass

	def make_choice(self, options):
		pass


class StupidAI(Personality):
	def __init__(self):
		pass

	def make_choice(self, options):
		return 0

class Human(Personality):
	def __init__(self):
		pass

	def make_choice(self, options):
		return int(stdin.readline())

