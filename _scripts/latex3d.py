#!/usr/bin/env python3

from dataclasses import dataclass
import math
import sys

import numpy as np


# katex ellipses … ⋮ ⋯ ⋱


def x_rotation(theta):
    return np.array(
        [
            [1, 0, 0],
            [0, math.cos(theta), -math.sin(theta)],
            [0, math.sin(theta), math.cos(theta)],
        ]
    )


def y_rotation(theta):
    return np.array(
        [
            [math.cos(theta), 0, math.sin(theta)],
            [0, 1, 0],
            [-math.sin(theta), 0, math.cos(theta)],
        ]
    )


def z_rotation(theta):
    return np.array(
        [
            [math.cos(theta), -math.sin(theta), 0],
            [math.sin(theta), math.cos(theta), 0],
            [0, 0, 1],
        ]
    )


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
    return [
        Entry(x=u - v, y=y, z=u + v - y, string=str(y + 1))
        for y in range(n)
        for v in range(y + 1)
        for u in range(y + 1)
    ]


def octahedron(n=3):
    entries = []
    for y in range(n):
        for v in range(y + 1):
            for u in range(y + 1):
                x = u - v
                z = u + v - y
                string = str(y + 1)
                entries.append(Entry(x, y, z, string))

                y2 = 2 * (n - 1) - y
                if y2 != y:
                    entries.append(Entry(x, y2, z, string))
    return entries


def octahedronx(n=3):
    return [
        Entry(x=e.y - (n - 1), y=e.x + n - 1, z=e.z, string=e.string)
        for e in octahedron(n)
    ]


def octahedronz(n=3):
    return [
        Entry(x=e.x, y=e.z + n - 1, z=e.y - (n - 1), string=e.string)
        for e in octahedron(n)
    ]


# first we rotate O=(1 1 1) to (0 1 √2):
TILT = y_rotation(-math.tau / 8)
# then we rotate (0 1 √2) to (0 -√3 0): (i.e. the highest possible point, in screen coordinates)
TILT = x_rotation(math.acos(-1 / math.sqrt(3))) @ TILT
# four vertices of a cube form a tetrahedron
# specifically, the vertices which are diagonally across faces from each other
# (so that the edge length of the tetrahedron is √2 for unit cube)
# We use a unit cube centered at the origin, rotated such that O is at the top:
O = TILT @ np.array([1, 1, 1]) / 2
A = TILT @ np.array([1, -1, -1]) / 2
B = TILT @ np.array([-1, 1, -1]) / 2
C = TILT @ np.array([-1, -1, 1]) / 2
OA = A - O
AB = B - A
BC = C - B
# turns to rotate ⋯ about z to align with tetrahedron edge:
DOTS_Z_TURNS = math.atan2(OA[1], OA[0]) / math.tau


def xyz(i, j, k):
    return O + k * OA + j * AB + i * BC


def tetrahedron(n=3, to=None):
    entries = [
        Entry(*xyz(i, j, k), str(k + 1))
        for k in range(n)
        for j in range(k + 1)
        for i in range(j + 1)
    ]

    if to:
        k = n  # penultimate layer
        for j, i in ((0, 0), (k, 0), (k, k)):
            p = xyz(i, j, k)
            dx, dy, dz = p - O
            y_turns = math.atan2(-dz, dx) / math.tau
            transform = f"translateX(-10px) rotateY({y_turns:.3f}turn) rotateZ({DOTS_Z_TURNS:.3f}turn)"
            entries.append(Entry(*p, "⋯", transform))

        k = n + 1  # ultimate layer
        a, b, c, d = (
            xyz(i, j, k)
            for j, i in ((0, 0), (k, 0), (k, k), ((k + 1) / 2, (k + 1) / 4))
        )
        entries += (Entry(*p, string=to) for p in (a, b, c, d))
        for start, end in ((a, b), (b, c), (c, a), (a, d), (b, d), (c, d)):
            p = (start + end) / 2
            dx, dy, dz = end - start
            y_turns = math.atan2(-dz, dx) / math.tau
            transform = f"translateX(-10px) rotateY({y_turns:.3f}turn)"
            entries.append(Entry(*p, "⋯", transform))

    return entries


def div(html, cls="", style=""):
    if cls:
        cls = f' class="{cls}"'
    if style:
        style = f' style="{style}"'
    return f"<div{cls}{style}>{html}</div>"


@dataclass
class Entry:
    x: int
    y: int
    z: int
    string: str
    transform: str = ""

    def html(self, k):
        t = f" {self.transform}" if self.transform else ""
        return div(
            # wrap normal entries (no custom transform) in an extra 'un-spinning' div:
            self.string if t else div(self.string),
            style=f"transform:translate3d({k*(self.x+1.9):.0f}px,{k*self.y:.0f}px,{k*self.z:.0f}px){t};",
        )


def latex3d(entries, cls="", style="", k=30):
    if cls:
        cls = f" {cls}"
    return div(
        "".join(e.html(k) for e in entries),
        cls=f"latex3d{cls}",
        style=f"width:{4*k}px;height:{4*k}px;{style}",
    )


K3 = 50
# numeric codes, because Katex breaks letters into multiple spans:
shapes = {
    "1222201": latex3d(pyramid()),
    "12222101": latex3d(octahedron()),
    "12222102": latex3d(octahedron(), cls="magenta"),
    "12222103": latex3d(octahedronx(), cls="orange"),
    "12222104": latex3d(octahedronz(), cls="tan"),
    "12222105": div(
        latex3d(
            octahedron(), k=K3, cls="magenta", style="position:absolute;left:-15px;"
        )
        + latex3d(
            octahedronx(), k=K3, cls="orange", style="position:absolute;left:0px;"
        )
        + latex3d(octahedronz(), k=K3, cls="tan", style="position:absolute;left:15px;"),
        style=f"position:relative;width:{4*K3}px;height:{4*K3}px;",
    ),
    "122201": latex3d(tetrahedron(4)),
    "122202": latex3d(tetrahedron(2, "n")),
}


for line in sys.stdin:
    for key, shape in shapes.items():
        line = line.replace(key, shape)
    print(line)
