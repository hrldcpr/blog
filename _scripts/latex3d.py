#!/usr/bin/env python3

import sys


def number(x, y, z, n):
  return f'<div class="number" style="transform: translate3d({x}px, {y}px, {z}px);">{n}</div>'

def latex3d(children):
  return f'<div class="latex3d">{"".join(children)}</div>'

PYRAMID0 = latex3d((number(100, 50, 0, 1),
                    number(50, 100, 50, 2),
                    number(150, 100, 50, 2),
                    number(50, 100, -50, 2),
                    number(150, 100, -50, 2)))


for line in sys.stdin:
  print(line.replace('12222', PYRAMID0))
