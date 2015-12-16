#this is a hack to get Processing to include necessary packages
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib')))
    import vector
    import newtonian

import math

pts = []
NUM_POINTS = 20

def setup():
    size(1024, 1024, OPENGL)
    global wind, gravity, fluid, moon, planet
    gravity = vector.PVect(0, .098)
    wind = newtonian.Wind(1, 1, width, height, offset=.05)
    fluid = newtonian.Fluid(width - 200, height - 100, width - 600, height - 200, 10)
    for i in xrange(NUM_POINTS):
        pt = newtonian.RandPoint(width, height, random(10))
        pts.append(pt)
        
    moon = newtonian.RandPoint(width, height, 10)
    planet = newtonian.RandPoint(width, height, 100)
    
def draw():
    background(255)
    stroke(0)
    fill(175)
    
    for i in xrange(NUM_POINTS):
        pts[i].applyForce(wind.getForce(pts[i].location.x, pts[i].location.y))
        pts[i].applyFriction(1, .1)
        fluid.applyDrag(pts[i])
        
        
    for i in xrange(NUM_POINTS):
        pts[i].step(1)
        pts[i].applyGravity(gravity)
        
    wind.step(1)
    planet.step(1)
    moon.step(1)
    checkEdges()
    for i in xrange(NUM_POINTS):
        ellipse(pts[i].location.x, pts[i].location.y, pts[i].mass, pts[i].mass)
    rect(fluid.x1, fluid.y1, fluid.x2-fluid.x1, fluid.y2-fluid.y1)

def checkEdges():
    for i in xrange(NUM_POINTS):
        if pts[i].location.x > width:
            pts[i].location.x = width
            pts[i].velocity.x *= -1
        elif pts[i].location.x < 0:
            pts[i].location.x = 0
            pts[i].velocity.x *= -1
        
        if pts[i].location.y > height:
            pts[i].location.y = height
            pts[i].velocity.y *= -1
        elif pts[i].location.y < 0:
            pts[i].location.y = 0
            pts[i].velocity.y *= -1
        