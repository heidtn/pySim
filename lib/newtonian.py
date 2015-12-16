from vector import PVect
import random
import math
import copy

class Point:
	def __init__(self, location, velocity, acceleration, mass = 1):
		self.location = location
		self.velocity = velocity
		self.acceleration = acceleration
		self.mass = mass
	def __str__(self):
		return "[" + str(self.location) + " " + str(self.velocity) + " " + str(self.acceleration) + "]"
	def step(self, time):
		self.velocity += self.acceleration
		self.location += self.velocity*time
		self.acceleration *= 0
	def applyForce(self, force):
		self.acceleration += force/self.mass
	def applyGravity(self, acceleration):
		self.acceleration += acceleration
	def applyFriction(self, normal, coefficient):
		friction = copy.deepcopy(self.velocity)
		friction.normalize() 
		friction *= -1
		friction *= coefficient*normal
		self.applyForce(friction)
	def applyDrag(self, density=.1):
		dragMag = density*(self.velocity.mag()**2)
		drag = copy.deepcopy(self.velocity)
		drag *= -1
		drag.normalize()
		drag *= dragMag
		self.applyForce(drag)
	def getForce(self):
		return self.mass * self.acceleration
	@staticmethod
	def applyGravitationalAttraction(A, B, G=1):
		forceMag = A.mass*B.mass*G/(self.vecBetween(A, B).mag()**2)
		forceVec = self.vecBetween(A, B).normalize()
		A.applyForce(forceVec*forceMag)
		B.applyForce(forceVec*(-1)*forceMag)
	@staticmethod
	def vecBetween(A, B):
		return A.location - B.location

class RandPoint(Point):
	def __init__(self, width, height, _mass):
		self.velocity = PVect(0, 0)
		self.location = PVect(random.randint(0, width), random.randint(0, height))
		self.acceleration = PVect(0, 0)
		self.mass = _mass

class Force:
	def __init__(self, _force):
		self.force = _force
	def step(self, time):
		pass
	def getForce(self):
		return self.force

class Fluid:
	def __init__(self, x1, y1, x2, y2, coefficient = .1):
		self.coefficient = .1
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
	def applyDrag(self, point):
		pt = point.location
		#print pt, self.x1, self.y1, self.x2, self.y2
		if(pt.x > self.x2 and pt.x < self.x1 and pt.y > self.y2 and pt.y < self.y1):
			point.applyDrag(self.coefficient)
			#print "dragged"


#adopted by code written by Ken Perlin (i.e. Perlin noise) and adapted by Stefan Gustavson
class Wind(Force):
	_grad3 = [
	[1,1,0], [-1,1,0], [1,-1,0], [-1,-1,0],
	[1,0,1], [-1,0,1], [1,0,-1], [-1,0,-1],
	[0,1,1], [0,-1,1], [0,1,-1], [0,-1,-1]]

	_perm = [
    151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,
    8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,
    35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,74,165,71,
    134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,
    55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,
    18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,
    250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,
    189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,43,
    172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,112,104,218,246,97,
    228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,
    107,49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,
    138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180,

    151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,
    8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,
    35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,74,165,71,
    134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,
    55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,
    18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,
    250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,
    189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,43,
    172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,112,104,218,246,97,
    228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,
    107,49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,
    138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]

	def __init__(self, _xmult, _ymult, _width, _height, offset = 0, octaves=3, persistence=.2, scale=1):
		self.xmult = _xmult
		self.ymult = _ymult
		self.octaves = octaves
		self.persistence = persistence
		self.scale = scale
		self.frame = 0
		self.width = float(_width)
		self.height = float(_height)
		self.windDir = PVect(self.xmult, self.ymult)
		self.offset = offset

	def step(self, time):
		self.frame += float(time)
		pass

	def getForce(self, x, y):
		mag = self.octave_noise_3d(self.octaves, self.persistence, self.scale, x/self.width, y/self.height, self.frame)
		mag += self.offset
		return self.windDir*mag

	def octave_noise_3d(self, octaves, persistence, scale, x, y, z):
		"""3D Multi-Octave Simplex noise.

		For each octave, a higher frequency/lower amplitude function will be added
		to the original. The higher the persistence [0-1], the more of each
		succeeding octave will be added.
		"""
		total = 0.0
		frequency = scale
		amplitude = 1.0

		# We have to keep track of the largest possible amplitude,
		# because each octave adds more, and we need a value in [-1, 1].
		maxAmplitude = 0.0;

		for i in range(octaves):
			total += self.raw_noise_3d( x * frequency,
							y * frequency,
							z * frequency) * amplitude
			frequency *= 2.0
			maxAmplitude += amplitude;
			amplitude *= persistence

		return total / maxAmplitude

	def raw_noise_3d(self, x, y, z):
		"""3D Raw Simplex noise."""
		# Noise contributions from the four corners
		n0, n1, n2, n3 = 0.0, 0.0, 0.0, 0.0

		# Skew the input space to determine which simplex cell we're in
		F3 = 1.0/3.0
		# Very nice and simple skew factor for 3D
		s = (x+y+z) * F3
		i = int(x + s)
		j = int(y + s)
		k = int(z + s)

		G3 = 1.0 / 6.0
		t = float(i+j+k) * G3
		# Unskew the cell origin back to (x,y,z) space
		X0 = i - t
		Y0 = j - t
		Z0 = k - t
		# The x,y,z distances from the cell origin
		x0 = x - X0
		y0 = y - Y0
		z0 = z - Z0

		# For the 3D case, the simplex shape is a slightly irregular tetrahedron.
		# Determine which simplex we are in.
		i1, j1, k1 = 0,0,0 # Offsets for second corner of simplex in (i,j,k) coords
		i2, j2, k2 = 0,0,0 # Offsets for third corner of simplex in (i,j,k) coords

		if x0 >= y0:
			if y0 >= z0: # X Y Z order
				i1 = 1
				j1 = 0
				k1 = 0
				i2 = 1
				j2 = 1
				k2 = 0
			elif x0 >= z0: # X Z Y order
				i1 = 1
				j1 = 0
				k1 = 0
				i2 = 1
				j2 = 0
				k2 = 1
			else: # Z X Y order
				i1 = 0
				j1 = 0
				k1 = 1
				i2 = 1
				j2 = 0
				k2 = 1
		else:
			if y0 < z0: # Z Y X order
				i1 = 0
				j1 = 0
				k1 = 1
				i2 = 0
				j2 = 1
				k2 = 1
			elif x0 < z0: # Y Z X order
				i1 = 0
				j1 = 1
				k1 = 0
				i2 = 0
				j2 = 1
				k2 = 1
			else: # Y X Z order
				i1 = 0
				j1 = 1
				k1 = 0
				i2 = 1
				j2 = 1
				k2 = 0

		# A step of (1,0,0) in (i,j,k) means a step of (1-c,-c,-c) in (x,y,z),
		# a step of (0,1,0) in (i,j,k) means a step of (-c,1-c,-c) in (x,y,z), and
		# a step of (0,0,1) in (i,j,k) means a step of (-c,-c,1-c) in (x,y,z), where
		# c = 1/6.
		x1 = x0 - i1 + G3      # Offsets for second corner in (x,y,z) coords
		y1 = y0 - j1 + G3
		z1 = z0 - k1 + G3
		x2 = x0 - i2 + 2.0*G3  # Offsets for third corner in (x,y,z) coords
		y2 = y0 - j2 + 2.0*G3
		z2 = z0 - k2 + 2.0*G3
		x3 = x0 - 1.0 + 3.0*G3 # Offsets for last corner in (x,y,z) coords
		y3 = y0 - 1.0 + 3.0*G3
		z3 = z0 - 1.0 + 3.0*G3

		# Work out the hashed gradient indices of the four simplex corners
		ii = int(i) & 255
		jj = int(j) & 255
		kk = int(k) & 255
		gi0 = self._perm[ii+self._perm[jj+self._perm[kk]]] % 12
		gi1 = self._perm[ii+i1+self._perm[jj+j1+self._perm[kk+k1]]] % 12
		gi2 = self._perm[ii+i2+self._perm[jj+j2+self._perm[kk+k2]]] % 12
		gi3 = self._perm[ii+1+self._perm[jj+1+self._perm[kk+1]]] % 12

		# Calculate the contribution from the four corners
		t0 = 0.6 - x0*x0 - y0*y0 - z0*z0
		if t0 < 0:
			n0 = 0.0
		else:
			t0 *= t0
			n0 = t0 * t0 * self.dot3d(self._grad3[gi0], x0, y0, z0)

		t1 = 0.6 - x1*x1 - y1*y1 - z1*z1
		if t1 < 0:
			n1 = 0.0
		else:
			t1 *= t1
			n1 = t1 * t1 * self.dot3d(self._grad3[gi1], x1, y1, z1)

		t2 = 0.6 - x2*x2 - y2*y2 - z2*z2
		if t2 < 0:
			n2 = 0.0
		else:
			t2 *= t2
			n2 = t2 * t2 * self.dot3d(self._grad3[gi2], x2, y2, z2)

		t3 = 0.6 - x3*x3 - y3*y3 - z3*z3
		if t3 < 0:
			n3 = 0.0
		else:
			t3 *= t3
			n3 = t3 * t3 * self.dot3d(self._grad3[gi3], x3, y3, z3)

		# Add contributions from each corner to get the final noise value.
		# The result is scaled to stay just inside [-1,1]
		return 32.0 * (n0 + n1 + n2 + n3)
		
	def dot3d(self, g, x, y, z):
		return g[0]*x + g[1]*y + g[2]*z
