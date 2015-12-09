from vector import PVect

class Point:
	def __init__(self, _location, _velocity, _acceleration):
		self.location = _location
		self.velocity = _velocity
		self.acceleration = _acceleration
	def __str__(self):
		return "[" + str(self.location) + " " + str(self.velocity) + " " + str(self.acceleration) + "]"
	def step(self, time):
		self.velocity += self.acceleration
		self.location += self.velocity