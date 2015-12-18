"""
This project simulates 2D particles repelled from each other, but attracted to a point source.
This is a newtonian example of negatively charged point masses attracted to a positively 
charged point.
"""


#this is a hack to get Processing to include necessary packages
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib')))
    from vector import PVect
    from newtonian import Point

import math

pts = []
NUM_POINTS = 100

def setup():
#    import sys
#    sys.path.append('/home/brizo/Documents/pySim/lib')
#    from vector import PVect
#    from newtonian import Point
    
    size(1024, 1024, OPENGL)
    for i in xrange(NUM_POINTS):
        vec = PVect(random(-2, 2), random(-2, 2))
        pts.append(Point(vec, vec, vec))
    
    
def draw():
    background(255);
    mouse = PVect()
    mouse.x = mouseX
    mouse.y = mouseY
    
    stroke(0)
    fill(175)
    
    for i in xrange(NUM_POINTS):
        dir = mouse - pts[i].location
        dir.normalize()
        dir *= .1
        pts[i].acceleration = dir
        for j in xrange(NUM_POINTS):
            if(i != j):
                dir = pts[i].location - pts[j].location
                dir.normalize()
                dir *= .001
                pts[i].acceleration += dir
                
        pts[i].step(1)
        ellipse(pts[i].location.x, pts[i].location.y, 2, 2)

