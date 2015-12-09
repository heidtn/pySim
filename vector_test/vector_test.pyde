import math

def setup():
    import sys
    sys.path.append('/home/brizo/Documents/pySim/lib')
    from vector import PVect
    from newtonian import Point
    
    size(1024, 1024, OPENGL)
    
    global pts, mouse
    pts = []
    
    mouse = PVect(0, 0)
    for i in xrange(20):
        vec = PVect(random(-2, 2), random(-2, 2))
        pts.append(Point(vec, vec, vec))
    
    
def draw():
    background(255);
    mouse.x = mouseX
    mouse.y = mouseY
    
    
    stroke(0)
    fill(175)
    
    for i in xrange(20):
        dir = mouse - pts[i].location
        dir.normalize()
        dir *= .1
        pts[i].acceleration = dir
        for j in xrange(20):
            if(i != j):
                dir = pts[i].location - pts[j].location
                dir.normalize()
                dir *= .001
                pts[i].acceleration += dir
                
        pts[i].step(1)
        ellipse(pts[i].location.x, pts[i].location.y, 2, 2)
    
    
    
 
