import math

class PVect:
	def __init__(self, _x = 0, _y = 0):
		self.x = _x
		self.y = _y
	def __add__(self, other):
		return PVector(self.x + other.x, self.y + other.y)
	def __sub__(self, other):
		return PVector(self.x - other.x, self.y - other.y)
	def __mul__(self, other):
		return PVector(self.x*other, self.y*other)
	def __div__(self, other):
		return PVector(self.x/other, self.y/other)
	def __str__(self):
		return str(self.x) + " " + str(self.y)
	def mag(self):
		return math.sqrt(self.x*self.x + self.y*self.y)
	def normalize(self):
		magnitude = self.mag()
		if(magnitude != 0):
			self.x /= magnitude
			self.y /= magnitude