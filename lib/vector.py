import math

class PVect:
	def __init__(self, x = 0, y = 0):
		self.x = float(x)
		self.y = float(y)
	def __add__(self, other):
		return PVect(self.x + other.x, self.y + other.y)
	def __sub__(self, other):
		return PVect(self.x - other.x, self.y - other.y)
	def __mul__(self, other):
		return PVect(self.x*other, self.y*other)
	def __div__(self, other):
		return PVect(self.x/other, self.y/other)
	def __str__(self):
		return str(self.x) + " " + str(self.y)
	def cross(self, other):
		return self.x*other.y - self.y*other.x
	def mag(self):
		return math.sqrt(self.x*self.x + self.y*self.y)
	def normalize(self):
		magnitude = self.mag()
		if(magnitude != 0):
			self.x /= magnitude
			self.y /= magnitude
		else:
			self.x = 0
			self.y = 0
	def heading(self):
		return math.atan2(self.x, self.y)