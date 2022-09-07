#!/usr/bin/env python3

from dataclasses import dataclass
import math
import re
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
    style: str = ""
    cls: str = ""

    def html(self, w: float, k: float) -> str:
        return div(
            div(self.text, self.cls, self.style),  # wrap text in an 'un-spinning' div
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


def ellipsis(start, end):
    return [Entry(*(start + i * (end - start) / 6), "⋅") for i in range(2, 5)]


def line(to: str):
    return [
        Entry(0, 0, 0, "1"),
        Entry(0, 1, 0, "2"),
        *ellipsis(np.array([0, 1, 0]), np.array([0, 3, 0])),
        Entry(0, 3, 0, to),
    ]


def line_(to: str):
    return [Entry(e.x, 3 - e.y, e.z, e.text) for e in line(to)]


HEIGHT_SIDE_RATIO = math.sin(math.tau / 3)


def xyz3(u: float, y: float):
    return np.array([(u - y / 2) / HEIGHT_SIDE_RATIO, y, 0])


def triangle(
    n: int = 3,
    to: str = "",
    text: str = "",
    to_multi: bool = False,
) -> list[Entry]:
    entries = [
        Entry(*xyz3(u, y), text or str(y + 1)) for y in range(n) for u in range(y + 1)
    ]

    if to:
        # ends of three horizontal layers:
        # k=n-1 (layer 1) is the last numeric layer
        # k=n+1 (layer 2) is the (pen)ultimate symbolic layer
        # k=n+2 (layer 3, only used if to_multi) is the ultimate symbolic layer
        a1, b1, a2, b2, a3, b3 = (
            xyz3(u, y) for y in (n - 1, n + 1, n + 2) for u in (0, y)
        )
        ab3 = a3 + [1, 0, 0]
        ba3 = b3 - [1, 0, 0]

        # ellipses:
        for start, end in [(a1, a2), (b1, b2), (a2, b2)] + (
            [(ab3, ba3)] if to_multi else []
        ):
            entries += ellipsis(start, end)

        entries += (
            Entry(
                *p,
                text or (f"{to}–1" if to_multi else to),
                style="font-size:0.6em;" if to_multi else "",
            )
            for p in [a2, b2]
        )

        if to_multi:
            entries += (Entry(*p, text=to) for p in [a3, ab3, b3, ba3])

    for e in entries:
        t = re.sub("<.*?>", "", e.text)  # strip html
        e.x -= 0.1 * (len(t) - 1)  # center multi-character entries

    return entries


def triangle_(
    i: int,
    n: int = 3,
    to: str = "",
    text: str = "",
    to_multi: bool = False,
) -> list[Entry]:
    entries = triangle(n, to, text, to_multi)
    if to:
        n += 3 if to_multi else 2
    center = np.array([0, 2 * (n - 1) / 3, 0])  # centroid is at 2/3 of altitude

    def rotate(x):
        return (
            z_rotation(-i * math.tau / 3) @ (x - center) + center
        )  # rotate about centroid

    return [Entry(*(rotate([e.x, e.y, e.z])), e.text, e.style) for e in entries]


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


def xyz4(i: float, j: float, k: float):
    return O + k * OA + j * AB + i * BC


def tetrahedron(
    n: int = 3,
    to: str = "",
    text: str = "",
    to_multi: bool = False,
    to_center: bool = False,
) -> list[Entry]:
    entries = [
        Entry(*xyz4(i, j, k), text or str(k + 1))
        for k in range(n)
        for j in range(k + 1)
        for i in range(j + 1)
    ]

    if to:
        # corners and centers of three horizontal triangular layers:
        # k=n-1 (layer 1) is the last numeric layer
        # k=n+1 (layer 2) is the (pen)ultimate symbolic layer
        # k=n+2 (layer 3, only used if to_multi) is the ultimate symbolic layer
        a1, b1, c1, d1, a2, b2, c2, d2, a3, b3, c3, d3 = (
            xyz4(i, j, k)
            for k in (n - 1, n + 1, n + 2)
            for j, i in ((0, 0), (k, 0), (k, k), (2 * k / 3, k / 3))
            # ((⅔,⅓) is because the center of an equilateral triangle is 2/3 along the altitude,
            # but we follow the edges so have to offset along other edge by half that again)
        )
        ab3 = a3 + AB
        ba3 = b3 - AB
        bc3 = b3 + BC
        cb3 = c3 - BC
        ac3 = a3 + AB + BC
        ca3 = c3 - AB - BC

        # ellipses:
        for start, end in (
            [(a1, a2), (b1, b2), (c1, c2)]
            + (
                [(ab3, ba3), (bc3, cb3), (ca3, ac3)]
                if to_multi
                else [(a2, b2), (b2, c2), (c2, a2)]
            )
            + ([(d1, d2)] if to_center else [])
        ):
            entries += ellipsis(start, end)

        entries += (
            Entry(
                *p,
                text or (f"{to}–1" if to_multi else to),
                style="font-size:0.8em;" if to_multi else "",
            )
            for p in [a2, b2, c2] + ([d2] if to_center else [])
        )

        if to_multi:
            entries += (
                Entry(*p, text=to)
                for p in [a3, ab3, ac3, b3, ba3, bc3, c3, ca3, cb3]
                + ([d3] if to_center else [])
            )

    return entries


def tetrahedron_(
    i: int,
    n: int = 3,
    to: str = "",
    text: str = "",
    to_multi: bool = False,
    to_center: bool = False,
) -> list[Entry]:
    entries = tetrahedron(n, to, text, to_multi, to_center)
    if to:
        n += 3 if to_multi else 2
    center = np.array([0, 3 * (n - 1) / 4, 0])  # centroid is at 3/4 of altitude

    def rotate(x):
        tilt = y_rotation(-math.tau / 6)  # rotate left corner to front
        tilt = x_rotation(-VERTEX_CENTER_VERTEX_ANGLE) @ tilt  # rotate front to top
        tilt = y_rotation(-i * math.tau / 3) @ tilt  # rotate to one of three symmetries
        return tilt @ (x - center) + center  # rotate about centroid

    return [Entry(*(rotate([e.x, e.y, e.z])), e.text, e.style) for e in entries]


def latex3d(
    entries: list[Entry],
    cls: str = "",
    style: str = "",
    k: float = 1.0,  # scales geometry
    k_text: float = 1.0,  # scales text
    dh: float = 0.0,
) -> str:
    w = 1 + 2 * max(math.hypot(e.x, e.z) for e in entries)
    h = max(e.y for e in entries) - 0.5 + dh
    if cls == "flat":
        h -= 0.3  # better vertical centering for 2d shapes
    if cls:
        cls = f" {cls}"
    return div(
        "".join(e.html(w, k / k_text) for e in entries),
        cls=f"latex3d{cls}",
        style=f"font-size:{k_text:.2f}em;width:{w*k/k_text:.2f}em;height:{h*k/k_text:.2f}em;{style}",
    )


def latex2d(entries: list[Entry], k_text: float = 1.0) -> str:
    return latex3d(entries, k_text=k_text, cls="flat")


def classed(entries: list[Entry], classes: dict[int, str]):
    return [
        Entry(e.x, e.y, e.z, e.text, e.style, cls=classes[i]) if i in classes else e
        for i, e in enumerate(entries)
    ]


N = '<span class="mathnormal">n</span>'
NN1 = f"2{N}+1"
NNN1 = f"3{N}+1"


def triangle2n1():
    entries = triangle(2, NN1, NN1)
    # adjust the second row to avoid overlap:
    entries[1].x -= 0.3
    entries[2].x += 0.3
    return entries


BLUE = "blue"
MAGENTA = "magenta"
ORANGE = "orange"
PURPLE = "purple"
TAN = "tan"
# numeric codes, because Katex breaks letters into multiple spans:
shapes = {
    "1201": latex2d(line(N)),
    "1202": latex2d(line_(N)),
    "12200": latex2d(triangle(4)),
    "12201": latex2d(triangle(2, N)),
    "12202": latex2d(triangle_(1, 2, N)),
    "12203": latex2d(triangle_(2, 2, N)),
    "12204": latex2d(triangle2n1(), k_text=0.6),
    "12291": latex2d(classed(triangle(4), {0: TAN, 4: ORANGE, 8: MAGENTA})),
    "12292": latex2d(classed(triangle_(1, 4), {9: TAN, 4: ORANGE, 3: MAGENTA})),
    "12293": latex2d(classed(triangle_(2, 4), {6: TAN, 4: ORANGE, 2: MAGENTA})),
    "12294": latex2d(classed(triangle(4, text="9"), {0: TAN, 4: ORANGE, 8: MAGENTA})),
    "1222200": latex3d(pyramid()),
    "12222101": latex3d(octahedron(), dh=-1.0),
    "12222102": latex3d(octahedronx(), dh=-1.0),
    "12222103": latex3d(octahedronz(), dh=-1.0),
    "12222104": div(
        latex3d(octahedron(), k=1.5, cls=TAN, style="position:absolute;left:-0.5em;")
        + latex3d(octahedronx(), k=1.5, cls=ORANGE, style="position:absolute;left:0;")
        + latex3d(
            octahedronz(), k=1.5, cls=MAGENTA, style="position:absolute;left:0.5em;"
        ),
        style=f"position:relative;transform-style:preserve-3d;top:-1em;width:8.5em;height:5em;",
    ),
    "122200": latex3d(tetrahedron(4)),
    "122201": latex3d(tetrahedron(2, N)),
    "122202": latex3d(tetrahedron_(0, 2, N)),
    "122203": latex3d(tetrahedron_(1, 2, N)),
    "122204": latex3d(tetrahedron_(2, 2, N)),
    "122205": latex3d(tetrahedron(2, NNN1, NNN1), k_text=0.7),
    "122291": latex3d(classed(tetrahedron(), {0: TAN, 1: ORANGE, 4: MAGENTA})),
    "122292": latex3d(classed(tetrahedron_(0), {9: TAN, 6: ORANGE, 4: MAGENTA})),
    "122293": latex3d(classed(tetrahedron_(1), {9: TAN, 8: ORANGE, 7: MAGENTA})),
    "122294": latex3d(classed(tetrahedron_(2), {9: TAN, 3: ORANGE, 0: MAGENTA})),
    "122295": latex3d(classed(tetrahedron(text="10"), {0: TAN, 1: ORANGE, 4: MAGENTA})),
}
shapes = {f">{k}<": f">{v}<" for k, v in shapes.items()}  # only match span content

if __name__ == "__main__":
    for line in sys.stdin:
        for key, shape in shapes.items():
            line = line.replace(key, shape)
        print(line)
