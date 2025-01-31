import pygame
import numpy as np
from typing import List,Tuple, Union
from typing_extensions import Self
from scipy.spatial import ConvexHull


Point = Tuple[float,float]



class Shape:
    def __init__(this, points:List[Union[Point,np.ndarray]], color:pygame.Color):
        this.points = np.concatenate([ np.asarray([p]) for p in points ],axis=0)
        this.color = color

    def draw(this, surface:pygame.surface):
        pygame.draw.polygon(surface, this.color, this.points)

    def move(this,delta:Union[Point|pygame.Vector2]) -> Self:

        this.points = np.stack(
            [(x + delta.x, y + delta.y) if isinstance(delta,pygame.Vector2) else (x + delta[0], y + delta[1]) for x, y in this.points],
            axis=0)

        return this

    def scale(this,factor:float) -> Self:
        return this.transform(np.asarray([[factor,0],[0,factor]]))

    def rotate(this,angle:float)->Self:
        cos = np.cos(np.deg2rad(angle))
        sin = np.sin(np.deg2rad(angle))

        return this.transform(np.asarray([[cos,-sin],[sin,cos]]))

    def transform(this,matrix:np.ndarray) -> Self:


        centre = this.points.mean(axis=0)

        new_points = ((this.points-centre) @ matrix.transpose()) + centre

        this.points = new_points

        return this


    def __contains__(this, other:Self) -> bool:
        return gjk(this,other)

    def get_furthest_point(this,v:np.ndarray) -> np.ndarray:
        return np.asarray(max(this.points, key=lambda x: np.dot(x, v)))


class MinkowskiDifferenceShape(Shape):

    def __init__(this,A:Shape,B:Shape,color:pygame.Color):
        p = np.asarray([ (a[0]-b[0],a[1]-b[1]) for a in A.points for b in B.points ])
        hull = ConvexHull(p)


        super().__init__([p[i] for i in hull.vertices],color)



class CollisionException(Exception):
    ...


#
def same_direction(u:np.ndarray,v:np.ndarray) -> bool:
    return np.dot(u,v)>0

def support(A:Shape,B:Shape,v:np.ndarray) -> np.ndarray:
    return A.get_furthest_point(v) - B.get_furthest_point(-v)

def orthogonal(v:np.ndarray):
    return np.asarray([-v[1],v[0]])



def triple_product(x:np.ndarray,y:np.ndarray) -> np.ndarray:
    x3 = np.asarray([x[0],x[1], 0])
    y3 = np.asarray([y[0], y[1], 0])

    return np.cross(np.cross(x3,y3),x3)[:2]
def next_direction(triangle):

    if len(triangle) == 3:
        a,b,c = triangle
        ab = b - a
        ao = -a

        new_dir = triple_product(ab,ao)

        if not same_direction(new_dir, ao):
            triangle.pop(2)  # Keep only points 'a' and 'b'
            return new_dir
        else:
            ac = c - a
            new_dir = triple_product(ac,ao)
            if not same_direction(new_dir, ao):
                triangle.pop(1)  # Keep only points 'a' and 'c'
                return new_dir

    elif len(triangle) == 2:
        b,a = triangle
        ab = b - a
        ao = -a
        direction = triple_product(ab,ao)

        return direction


    raise CollisionException()


import matplotlib.pyplot as plt
def gjk(A:Shape, B:Shape):


    direction = np.array([1, 0])
    triangle = [support(A,B,direction)]
    direction = -triangle[0]

    try:
        last_point = None
        while True:
            new_point = support(A,B,direction)

            if (not same_direction(new_point, direction)) or (new_point==last_point).all():
                return False

            triangle.append(new_point)

            direction = next_direction(triangle)
            last_point = new_point



    except CollisionException:
        return True


