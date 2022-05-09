#!/usr/bin/env python3

from dataclasses import dataclass
import math
import sys

import numpy as np


def div(html: str, cls: str = "", style: str = "") -> str:
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
    text: str

    def html(self, k: float) -> str:
        w = 4 * k
        return div(
            div(self.text),  # wrap text in an extra 'un-spinning' div
            style=f"transform:translate3d({w/2+k*self.x:.0f}px,{k*self.y:.0f}px,{k*self.z:.0f}px);",
        )


def x_rotation(theta: float):
    return np.array(
        [
            [1, 0, 0],
            [0, math.cos(theta), -math.sin(theta)],
            [0, math.sin(theta), math.cos(theta)],
        ]
    )


def y_rotation(theta: float):
    return np.array(
        [
            [math.cos(theta), 0, math.sin(theta)],
            [0, 1, 0],
            [-math.sin(theta), 0, math.cos(theta)],
        ]
    )


def z_rotation(theta: float):
    return np.array(
        [
            [math.cos(theta), -math.sin(theta), 0],
            [math.sin(theta), math.cos(theta), 0],
            [0, 0, 1],
        ]
    )


def pyramid(n: int = 3) -> list[Entry]:
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
        Entry(x=u - v, y=y, z=u + v - y, text=str(y + 1))
        for y in range(n)
        for v in range(y + 1)
        for u in range(y + 1)
    ]


def octahedron(n: int = 3) -> list[Entry]:
    entries = pyramid(n)
    # double everything except the last layer:
    entries += (
        Entry(x=e.x, y=2 * (n - 1) - e.y, z=e.z, text=e.text)
        for e in entries
        if e.y < n - 1
    )
    return entries


def octahedronx(n: int = 3) -> list[Entry]:
    return [
        Entry(x=e.y - (n - 1), y=e.x + n - 1, z=e.z, text=e.text) for e in octahedron(n)
    ]


def octahedronz(n: int = 3) -> list[Entry]:
    return [
        Entry(x=e.x, y=e.z + n - 1, z=e.y - (n - 1), text=e.text) for e in octahedron(n)
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


def xyz(i: float, j: float, k: float):
    return O + k * OA + j * AB + i * BC


def tetrahedron(n: int = 3, to: str = "") -> list[Entry]:
    entries = [
        Entry(*xyz(i, j, k), str(k + 1))
        for k in range(n)
        for j in range(k + 1)
        for i in range(j + 1)
    ]

    if to:
        # corners and centers of last numeric layer and last layer:
        # (the center of an equilateral triangle is 2/3 along the altitude,
        # but we follow the edges so have to offset along other edge by half that again)
        a1, b1, c1, d1, a2, b2, c2, d2 = (
            xyz(i, j, k)
            for k in (n - 1, n + 1)
            for j, i in ((0, 0), (k, 0), (k, k), (2 * k / 3, k / 3))
        )

        entries += (Entry(*p, text=to) for p in (a2, b2, c2, d2))

        # ellipses:
        for start, end in (
            (a1, a2),
            (b1, b2),
            (c1, c2),
            (d1, d2),
            (a2, b2),
            (b2, c2),
            (c2, a2),
        ):
            for i in range(2, 5):
                p = start + i * (end - start) / 6
                entries.append(Entry(*p, "⋅"))

    return entries


def latex3d(entries: list[Entry], cls: str = "", style: str = "", k: float = 30) -> str:
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
    "1222200": latex3d(pyramid()),
    "12222100": latex3d(octahedron()),
    "12222101": latex3d(octahedron(), cls="magenta"),
    "12222102": latex3d(octahedronx(), cls="orange"),
    "12222103": latex3d(octahedronz(), cls="tan"),
    "12222104": div(
        latex3d(
            octahedron(), k=K3, cls="magenta", style="position:absolute;left:-15px;"
        )
        + latex3d(
            octahedronx(), k=K3, cls="orange", style="position:absolute;left:0px;"
        )
        + latex3d(octahedronz(), k=K3, cls="tan", style="position:absolute;left:15px;"),
        style=f"position:relative;width:{4*K3}px;height:{4*K3}px;",
    ),
    "122200": latex3d(tetrahedron(4)),
    "122201": latex3d(tetrahedron(2, "n")),
}


for line in sys.stdin:
    for key, shape in shapes.items():
        line = line.replace(key, shape)
    print(line)
