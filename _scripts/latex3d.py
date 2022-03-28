#!/usr/bin/env python3

import math
import sys


# katex ellipses … ⋮ ⋯ ⋱

def pyramid(n=3, to=None):
  # 90° internal angles, i.e. slope (tangent) of 1:1
  #
  #     3         3   3   3
  #   3 2 3         2   2
  # 3 2 1 2 3  ≠  3   1   3
  #   3 2 3         2   2
  #     3         3   3   3
  #     ✓             x
  #
  if to: n += 2
  xyzcts = []
  for y in range(n):
    for v in range(y+1):
      for u in range(y+1):
        x = u-v
        z = u+v-y
        transform = ''
        if to and y==n-1:
          if 1<u<y-1 or 1<v<y-1: continue  # corners only
          c = 'n'
        elif to and y==n-2:
          if 0<u<y or 0<v<y: continue  # corners only
          turns = math.atan2(-z, x) / math.tau
          c = '⋯'
          transform = f' translateX(-10px) rotateY({turns:.2f}turn) rotateZ(0.125turn)'
        else:
          c = y+1
        xyzcts.append((x, y, z, c, transform))
  return xyzcts

def octahedron(n=3):
  xyzcts = []
  for y in range(n):
    for v in range(y+1):
      for u in range(y+1):
        x = u-v
        z = u+v-y
        c = y+1
        xyzcts.append((x, y, z, c, ''))
        y2 = 2*(n-1) - y
        if y != y2: xyzcts.append((x, y2, z, c, ''))
  return xyzcts


K = 30
W = H = 4*K
DX = W/2 - 0.1*K  # includes character-centering offset
DY = 0*K
DZ = 0*K

def character(x, y, z, c, transform=None):
  if not transform: transform = ' rotateY(var(--untheta))'
  return f'<div style="transform:translate3d({K*x+DX}px,{K*y+DY}px,{K*z+DZ}px){transform};">{c}</div>'

def latex3d(*xyzcts):
  return f'<div class="latex3d" style="width:{W}px;height:{H}px;">{"".join(character(*xyzct) for xyzct in xyzcts)}</div>'


# numeric codes, because Katex breaks letters into multiple spans:
shapes = dict((k, latex3d(*v)) for k,v in (
  ('1222201', pyramid()),
  ('12222101', octahedron()),
  ('12222102', ((x,y,z,c,' rotateY(var(--untheta)) rotateX(-0.25turn)') for x,y,z,c,_ in octahedron())),
  ('12222103', ((x,y,z,c,' rotateY(var(--untheta)) rotateZ(-0.25turn)') for x,y,z,c,_ in octahedron())),
  ('12222104', list(octahedron())+[(x,y,z,c,' rotateY(var(--untheta)) rotateX(-0.25turn)') for x,y,z,c,_ in octahedron()]+[(x,y,z,c,' rotateY(var(--untheta)) rotateZ(-0.25turn)') for x,y,z,c,_ in octahedron()]),
))


for line in sys.stdin:
  for key,shape in shapes.items():
    line = line.replace(key, shape)
  print(line)
