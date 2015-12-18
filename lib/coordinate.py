import newtonian
from vector import PVect
import math

class RigidBody:
	__init__(self, width=0, height=0, bounded=False):
		self.objects = []
		self.angle = 0.0
		self.COM = PVect(0, 0)
		self.velocity = PVect(0, 0)
		self.location = PVect(0, 0)
		self.totalMass = 0
		self.torque = 0
	def addBody(self, body):
		self.objects.append(body)
		self.calcCOM()
	def calcCOM(self):
		mass = 0
		xnum = 0
		ynum = 0
		for obj in self.objects:
			mass += obj.mass
			xnum += obj.mass*obj.location.x
			ynum += obj.mass*obj.location.y
		self.totalMass = mass
		self.COM.x = xnum/mass
		self.COM.y = ynum/mass
		self.location.x = self.COM.x
		self.location.y = self.COM.y
	def calcForces(self):
		self.torque = 0
		self.forces = PVect(0, 0)
		for obj in self.objects:
			self.torque += obj.getForce().cross(self.COM - obj.location)
			self.forces += obj.getForce()
	def step(self, time):
		self.calcForces()



	def comDist(self, obj):
		return math.sqrt(self.COM.x)

class Sphere(newtonian.Point):
	__init__(self, x, y, mass, width, height):
		newtonian.Point().__init__(self, PVect(x, y), PVect(0, 0), PVect(0, 0), mass)
		self.width = width
		self.height = height

class Rod:
	__init__(self, x, y, length):
		self.location = PVect(x, y)
		self.mass = 0
		self.length = length
	def getForce():
		return PVect(0, 0)

