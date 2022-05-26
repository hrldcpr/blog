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
    x: float
    y: float
    z: float
    text: str

    def html(self, w: float, k: float) -> str:
        return div(
            div(self.text),  # wrap text in an extra 'un-spinning' div
            style=f"transform:translate3d({k*(w/2+self.x):.2f}em,{k*self.y:.2f}em,{k*self.z:.2f}em);",
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
        for e in reversed(entries)
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


FACE_VERTEX_EDGE_ANGLE = math.acos(-1 / math.sqrt(3))
VERTEX_CENTER_VERTEX_ANGLE = math.acos(-1 / 3)
# first we rotate O=(1 1 1) to (0 1 √2):
TILT = y_rotation(-math.tau / 8)
# then we rotate (0 1 √2) to (0 -√3 0): (i.e. the highest possible point, in screen coordinates)
TILT = x_rotation(FACE_VERTEX_EDGE_ANGLE) @ TILT
# four vertices of a cube form a tetrahedron
# specifically, the vertices which are diagonally across faces from each other
# (so that the edge length of the tetrahedron is √2 for unit cube)
# We use a cube centered at the origin, rotated such that O is at the top:
O = TILT @ np.array([1, 1, 1])
A = TILT @ np.array([1, -1, -1])
B = TILT @ np.array([-1, 1, -1])
C = TILT @ np.array([-1, -1, 1])
# offset and scale such that O.y=0 and A.y=B.y=C.y=1:
O, A, B, C = ((x - O) / (A[1] - O[1]) for x in (O, A, B, C))
OA = A - O
AB = B - A
BC = C - B


def xyz(i: float, j: float, k: float):
    return O + k * OA + j * AB + i * BC


def tetrahedron(
    n: int = 3, to: str = "", text: str = "", to_center: bool = True
) -> list[Entry]:
    entries = [
        Entry(*xyz(i, j, k), text or str(k + 1))
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

        # ellipses:
        entries += (
            Entry(*(start + i * (end - start) / 6), "⋅")
            for start, end in [
                (a1, a2),
                (b1, b2),
                (c1, c2),
                (a2, b2),
                (b2, c2),
                (c2, a2),
            ]
            + ([(d1, d2)] if to_center else [])
            for i in range(2, 5)
        )

        entries += (
            Entry(*p, text=to) for p in [a2, b2, c2] + ([d2] if to_center else [])
        )

    return entries


def tetrahedron_(i: int, n: int = 3, to: str = "") -> list[Entry]:
    entries = tetrahedron(n, to)
    if to:
        n += 2
    center = np.array([0, 3 * (n - 1) / 4, 0])  # centroid is at 3/4 of altitude

    def rotate(x):
        tilt = y_rotation(-math.tau / 6)  # rotate left corner to front
        tilt = x_rotation(-VERTEX_CENTER_VERTEX_ANGLE) @ tilt  # rotate front to top
        tilt = y_rotation(-i * math.tau / 3) @ tilt  # rotate to one of three symmetries
        return tilt @ (x - center) + center  # rotate about centroid

    return [Entry(*(rotate([e.x, e.y, e.z])), e.text) for e in entries]


def latex3d(
    entries: list[Entry],
    cls: str = "",
    style: str = "",
    k: float = 1.0,  # scales geometry
    k_text: float = 1.0,  # scales text
) -> str:
    w = 1 + 2 * max(math.hypot(e.x, e.z) for e in entries)
    h = max(e.y for e in entries)
    if cls:
        cls = f" {cls}"
    return div(
        "".join(e.html(w, k / k_text) for e in entries),
        cls=f"latex3d{cls}",
        style=f"font-size:{k_text:.2f}em;width:{w*k/k_text:.2f}em;height:{h*k/k_text:.2f}em;{style}",
    )


K3 = 1.5
# numeric codes, because Katex breaks letters into multiple spans:
shapes = {
    "1222200": latex3d(pyramid()),
    "12222100": latex3d(octahedron()),
    "12222101": latex3d(octahedron(), cls="magenta"),
    "12222102": latex3d(octahedronx(), cls="orange"),
    "12222103": latex3d(octahedronz(), cls="tan"),
    "12222104": div(
        latex3d(
            octahedron(), k=K3, cls="magenta", style="position:absolute;left:-0.5em;"
        )
        + latex3d(octahedronx(), k=K3, cls="orange", style="position:absolute;left:0;")
        + latex3d(
            octahedronz(), k=K3, cls="tan", style="position:absolute;left:0.5em;"
        ),
        style=f"position:relative;width:{4*K3:.2f}em;height:{4*K3:.2f}em;",
    ),
    "122200": latex3d(tetrahedron(4)),
    "122201": latex3d(tetrahedron(2, "n")),
    "122202": latex3d(tetrahedron_(0, 2, "n")),
    "122203": latex3d(tetrahedron_(1, 2, "n")),
    "122204": latex3d(tetrahedron_(2, 2, "n")),
    "122205": latex3d(tetrahedron(2, "3n+1", "3n+1"), k_text=0.7),
}

if __name__ == "__main__":
    for line in sys.stdin:
        for key, shape in shapes.items():
            line = line.replace(key, shape)
        print(line)
