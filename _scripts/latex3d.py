#!/usr/bin/env python3

import sys


def pyramid(n=3):
  # 90° internal angles, i.e. slope (tangent) of 1:1
  #
  #     3         3   3   3
  #   3 2 3         2   2
  # 3 2 1 2 3  ≠  3   1   3
  #   3 2 3         2   2
  #     3         3   3   3
  #     ✓             x
  #
  xyzcs = []
  for y in range(n):
    for v in range(y+1):
      for u in range(y+1):
        xyzcs.append((u-v, y, u+v-y, y+1))
  return xyzcs

def octahedron():
  return

def octahedron3a():
  return

def octahedron3b():
  return

def octahedron3c():
  return

def octahedron3abc():
  return

def tetrahedron():
  return

def tetrahedronb():
  return

def tetrahedronc():
  return


K = 50
DX = 1.9*K  # includes character-centering offset
DY = 1*K
DZ = 0*K

def character(x, y, z, c):
  return f'<div style="transform:translate3d({K*x+DX}px,{K*y+DY}px,{K*z+DZ}px);">{c}</div>'

def latex3d(*xyzcs):
  return f'<div class="latex3d">{"".join(character(*xyzc) for xyzc in xyzcs)}</div>'


# numeric codes, because Katex breaks letters into multiple spans:
shapes = dict((k, latex3d(*v)) for k,v in (
  ('1222201', pyramid()),
))


for line in sys.stdin:
  for key,shape in shapes.items():
    print(line.replace(key, shape))
