#!/usr/bin/env python
#
# Transform the 3D cyclone model as exported from cyclone.scad into a
# flat shape for conversion into DXF. 
#
import sys

class Vertex:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        self.key = (float(x), float(y), float(z))

    def transform(self, f):
        x, y, z = f(self.x, self.y, self.z)
        self.x, self.y, self.z = x, y, z
        self.key = (float(x), float(y), float(z))

class Normal:
    def __init__(self, dx, dy, dz):
        self.dx, self.dy, self.dz = dx, dy, dz

class Facet:
    def __init__(self, normal, v1, v2, v3):
        self.normal = normal
        if v1.key < v2.key:
            if v1.key < v3.key:
                self.vertices = (v1, v2, v3)    #v1 is the smallest
            else:
                self.vertices = (v3, v1, v2)    #v3 is the smallest
        else:
            if v2.key < v3.key:
                self.vertices = (v2, v3, v1)    #v2 is the smallest
            else:
                self.vertices = (v3, v1, v2)    #v3 is the smallest

    def key(self):
        return (self.vertices[0].x, self.vertices[0].y, self.vertices[0].z,
                self.vertices[1].x, self.vertices[1].y, self.vertices[1].z,
                self.vertices[2].x, self.vertices[2].y, self.vertices[2].z)

    def transform(self, f):
        for v in self.vertices:
            v.transform(f)

class STL:
    def __init__(self, fname):
        self.facets = []

        f = open(fname)
        words = [s.strip() for s in f.read().split()]
        f.close()

        if words[0] == 'solid':
            i = words.index('facet')
	    self.name = " ".join(words[1:i])
            while words[i] == 'facet':
                norm = Normal(words[i + 2],  words[i + 3],  words[i + 4])
                v1   = Vertex(words[i + 8],  words[i + 9],  words[i + 10])
                v2   = Vertex(words[i + 12], words[i + 13], words[i + 14])
                v3   = Vertex(words[i + 16], words[i + 17], words[i + 18])
                i += 21
                self.facets.append(Facet(norm, v1, v2, v3))
        else:
            print "Not an OpenSCAD ascii STL file"
            sys.exit(1)

    def canonicalise(self):
        self.facets.sort(key = Facet.key)

    def transform(self, f):
        for facet in self.facets:
            facet.transform(f)

    def write(self, fname):
        f = open(fname,"wt")
        print >> f,'solid ' + self.name
        for facet in self.facets:
            print >> f, '  facet normal %s %s %s' % (facet.normal.dx, facet.normal.dy, facet.normal.dz)
            print >> f, '    outer loop'
            for vertex in facet.vertices:
                print >> f, '      vertex %s %s %s' % (vertex.x, vertex.y, vertex.z)
            print  >> f, '    endloop'
            print  >> f, '  endfacet'
        print >> f, 'endsolid ' + self.name
        f.close()

import math
from math import pi,sqrt

top_diameter=200.;
bottom_diameter=100.;
height=300.;

top_radius    =    top_diameter / 2;
bottom_radius = bottom_diameter / 2;
tga           = (top_radius - bottom_radius) / height;
total_height  = top_radius / tga;
bottom_height = total_height - height;

side_length   = sqrt(total_height*total_height + top_radius*top_radius)
flat_a = 2*pi * top_radius / side_length
sina   = top_radius / side_length

def conexform(x, y, z):
    x, y, z = float(x), float(y), float(z)
    nx, ny, nz = 0.0, 0.0, 0.0

    r1 = math.sqrt(x*x + y*y)
    r2 =  r1 / sina
    phi = flat_a * (math.atan2(y,x) ) / (2*pi)

    nx = r2 * math.cos(phi)
    ny = r2 * math.sin(phi)
    nz = (z * top_radius/total_height) - r1

    nx, ny, nz = str(nx), str(ny), str(nz)
    return (nx, ny, nz)

def deconify(fname):
    stl = STL(fname)
    stl.transform(conexform)
    stl.canonicalise()
    stl.write("flat-" + fname)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        deconify(sys.argv[1])
    else:
        print "usage: deconify file"
        sys.exit(1)
