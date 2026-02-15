import math


def dda_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    steps = max(abs(dx), abs(dy))

    if steps == 0:
        yield (round(x1), round(y1), 1.0)
        return

    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1

    for i in range(int(steps) + 1):
        yield (round(x), round(y), 1.0)
        x += x_inc
        y += y_inc


def bresenham_int_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    err = dx - dy

    x, y = x1, y1

    while True:
        yield (x, y, 1.0)

        if x == x2 and y == y2:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x += sx

        if e2 < dx:
            err += dx
            y += sy


def wu_line(x1, y1, x2, y2):

    def fpart(x):
        return x - math.floor(x)

    def rfpart(x):
        return 1 - fpart(x)

    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)

    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) < 0.001:
        if y1 > y2:
            y1, y2 = y2, y1
        x = round(x1)
        for y in range(int(y1), int(y2) + 1):
            yield (x, y, 1.0)
        return

    steep = abs(dy) > abs(dx)

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        dx, dy = dy, dx

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    gradient = dy / dx if abs(dx) > 0.001 else 1.0

    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = rfpart(x1 + 0.5)
    xpxl1 = int(xend)
    ypxl1 = int(math.floor(yend))

    if steep:
        yield (ypxl1, xpxl1, rfpart(yend) * xgap)
        yield (ypxl1 + 1, xpxl1, fpart(yend) * xgap)
    else:
        yield (xpxl1, ypxl1, rfpart(yend) * xgap)
        yield (xpxl1, ypxl1 + 1, fpart(yend) * xgap)

    intery = yend + gradient

    xend = round(x2)
    yend = y2 + gradient * (xend - x2)
    xgap = fpart(x2 + 0.5)
    xpxl2 = int(xend)
    ypxl2 = int(math.floor(yend))

    if steep:
        yield (ypxl2, xpxl2, rfpart(yend) * xgap)
        yield (ypxl2 + 1, xpxl2, fpart(yend) * xgap)
    else:
        yield (xpxl2, ypxl2, rfpart(yend) * xgap)
        yield (xpxl2, ypxl2 + 1, fpart(yend) * xgap)

    for x in range(xpxl1 + 1, xpxl2):
        if steep:
            yield (int(math.floor(intery)), x, rfpart(intery))
            yield (int(math.floor(intery)) + 1, x, fpart(intery))
        else:
            yield (x, int(math.floor(intery)), rfpart(intery))
            yield (x, int(math.floor(intery)) + 1, fpart(intery))
        intery += gradient
