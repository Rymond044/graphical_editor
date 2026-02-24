def bresenham_circle(cx, cy, r):
    r = max(1, round(r))
    x, y = 0, r
    d = 1 - r
    seen = set()

    while x <= y:
        points = [
            (cx + x, cy + y),
            (cx - x, cy + y),
            (cx + x, cy - y),
            (cx - x, cy - y),
            (cx + y, cy + x),
            (cx - y, cy + x),
            (cx + y, cy - x),
            (cx - y, cy - x),
        ]
        for px, py in points:
            if (px, py) not in seen:
                seen.add((px, py))
                yield (px, py, 1.0)

        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1


def midpoint_ellipse(cx, cy, a, b):
    a = max(1, round(a))
    b = max(1, round(b))

    a2 = a * a
    b2 = b * b
    seen = set()

    x, y = 0, b
    d1 = b2 - a2 * b + a2 / 4.0

    while 2 * b2 * x <= 2 * a2 * y:
        points = [
            (cx + x, cy + y),
            (cx - x, cy + y),
            (cx + x, cy - y),
            (cx - x, cy - y),
        ]
        for px, py in points:
            if (px, py) not in seen:
                seen.add((px, py))
                yield (px, py, 1.0)

        if d1 < 0:
            d1 += 2 * b2 * x + b2
        else:
            y -= 1
            d1 += 2 * b2 * x - 2 * a2 * y + b2
        x += 1

    d2 = b2 * (x + 0.5) ** 2 + a2 * (y - 1) ** 2 - a2 * b2

    while y >= 0:
        points = [
            (cx + x, cy + y),
            (cx - x, cy + y),
            (cx + x, cy - y),
            (cx - x, cy - y),
        ]
        for px, py in points:
            if (px, py) not in seen:
                seen.add((px, py))
                yield (px, py, 1.0)

        if d2 > 0:
            d2 += -2 * a2 * y + a2
        else:
            x += 1
            d2 += 2 * b2 * x - 2 * a2 * y + a2
        y -= 1


def midpoint_hyperbola(cx, cy, a, b, limit=None):
    a = max(1, round(a))
    b = max(1, round(b))

    if limit is None:
        limit = max(50, 5 * b)

    a2 = a * a
    b2 = b * b
    seen = set()

    x, y = a, 0

    while y <= limit:
        points = [
            (cx + x, cy + y),
            (cx - x, cy + y),
            (cx + x, cy - y),
            (cx - x, cy - y),
        ]
        for px, py in points:
            if (px, py) not in seen:
                seen.add((px, py))
                yield (px, py, 1.0)

        d = b2 * (x + 0.5) ** 2 - a2 * (y + 1) ** 2 - a2 * b2

        if d < 0:
            x += 1

        y += 1


def midpoint_parabola(cx, cy, p, direction=1, limit=None):
    p = max(1, round(abs(p)))
    if limit is None:
        limit = max(50, 5 * p)
    seen = set()
    dir = 1 if direction >= 0 else -1
    p2 = 2 * p
    p4 = 2 * p2

    x = 0
    y = 0
    d = 1 - p

    if (cx, cy) not in seen:
        seen.add((cx, cy))
        yield (cx, cy, 1.0)

    while y < p:
        px = cx + dir * x
        if (px, cy + y) not in seen:
            seen.add((px, cy + y))
            yield (px, cy + y, 1.0)
        if y > 0 and (px, cy - y) not in seen:
            seen.add((px, cy - y))
            yield (px, cy - y, 1.0)

        if d >= 0:
            x += 1
            d -= p2
        y += 1
        d += 2 * y + 1

    if d == 1:
        d = 1 - p4
    else:
        d = 1 - p2

    while x < limit:
        px = cx + dir * x
        if (px, cy + y) not in seen:
            seen.add((px, cy + y))
            yield (px, cy + y, 1.0)
        if y > 0 and (px, cy - y) not in seen:
            seen.add((px, cy - y))
            yield (px, cy - y, 1.0)

        if d < 0:
            y += 1
            d += 4 * y
        x += 1
        d -= p4
