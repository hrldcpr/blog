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
    if to:
        n += 2
    xyzcts = []
    for y in range(n):
        for v in range(y + 1):
            for u in range(y + 1):
                x = u - v
                z = u + v - y
                transform = ""
                if to and y == n - 1:
                    if 1 < u < y - 1 or 1 < v < y - 1:
                        continue  # corners only
                    c = "n"
                elif to and y == n - 2:
                    if 0 < u < y or 0 < v < y:
                        continue  # corners only
                    turns = math.atan2(-z, x) / math.tau
                    c = "⋯"
                    transform = f" translateX(-10px) rotateY({turns:.2f}turn) rotateZ(0.125turn)"
                else:
                    c = y + 1
                xyzcts.append((x, y, z, c, transform))
    return xyzcts


def octahedron(n=3):
    xyzcts = []
    for y in range(n):
        for v in range(y + 1):
            for u in range(y + 1):
                x = u - v
                z = u + v - y
                c = y + 1
                xyzcts.append((x, y, z, c, ""))
                y2 = 2 * (n - 1) - y
                if y != y2:
                    xyzcts.append((x, y2, z, c, ""))
    return xyzcts


def octahedronx(n=3):
    return [(y - (n - 1), x + n - 1, z, c, t) for x, y, z, c, t in octahedron(n)]


def octahedronz(n=3):
    return [(x, z + n - 1, y - (n - 1), c, t) for x, y, z, c, t in octahedron(n)]


def div(html, cls="", style=""):
    if cls:
        cls = f' class="{cls}"'
    if style:
        style = f' style="{style}"'
    return f"<div{cls}{style}>{html}</div>"


def character(x, y, z, c, transform, k):
    if not transform:
        c = div(c)  # wrap normal characters in an extra 'un-spinning' div
    return div(
        c, style=f"transform:translate3d({k*(x+1.9)}px,{k*y}px,{k*z}px){transform};"
    )


def latex3d(xyzcts, cls="", style="", k=30):
    if cls:
        cls = f" {cls}"
    return div(
        "".join(character(*xyzct, k) for xyzct in xyzcts),
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
}


for line in sys.stdin:
    for key, shape in shapes.items():
        line = line.replace(key, shape)
    print(line)
