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

def octahedronx(n=3):
  return [(y-(n-1), x+n-1, z, c, ' rotateY(var(--untheta)) translateX(-10px)') for x,y,z,c,t in octahedron(n)]

def octahedronz(n=3):
  return [(x, z+n-1, y-(n-1), c, ' rotateY(var(--untheta)) translateX(10px)') for x,y,z,c,t in octahedron(n)]


K = 30
W = H = 4*K
DX = W/2 - 0.1*K  # includes character-centering offset
DY = 0*K
DZ = 0*K

def div(html, cls=None, style=None):
  cls = f' class="{cls}"' if cls else ''
  style = f' style="{style}"' if style else ''
  return f'<div{cls}{style}>{html}</div>'

def character(x, y, z, c, transform=None):
  if not transform: transform = ' rotateY(var(--untheta))'
  return div(c, style=f'transform:translate3d({K*x+DX}px,{K*y+DY}px,{K*z+DZ}px){transform};')

def characters(xyzcts):
  return ''.join(character(*xyzct) for xyzct in xyzcts)

def latex3d(html):
  return div(html, cls='latex3d', style=f'width:{W}px;height:{H}px;')


# numeric codes, because Katex breaks letters into multiple spans:
shapes = {
  '1222201': latex3d(characters(pyramid())),
  '12222101': latex3d(characters(octahedron())),
  '12222102': latex3d(div(characters(octahedron()), cls='magenta')),
  '12222103': latex3d(div(characters(octahedronx()), cls='orange')),
  '12222104': latex3d(div(characters(octahedronz()), cls='tan')),
  '12222105': latex3d(div(characters(octahedron()), cls='magenta')
                      + div(characters(octahedronx()), cls='orange')
                      + div(characters(octahedronz()), cls='tan')),
}


for line in sys.stdin:
  for key,shape in shapes.items():
    line = line.replace(key, shape)
  print(line)
