import numpy as np


def hermite_curve(p0, p1, m0, m1, steps=20):
    M = np.array([[2, -2, 1, 1], [-3, 3, -2, -1], [0, 0, 1, 0], [1, 0, 0, 0]])

    Gx = np.array([p0[0], p1[0], m0[0], m1[0]], dtype=float)
    Gy = np.array([p0[1], p1[1], m0[1], m1[1]], dtype=float)

    Cx = M.dot(Gx)
    Cy = M.dot(Gy)

    for i in range(steps + 1):
        t = i / steps if steps > 0 else 0.0
        T = np.array([t**3, t**2, t, 1.0])
        x: float = float(T.dot(Cx))
        y: float = float(T.dot(Cy))
        yield (round(x), round(y), 1.0)


def bezier_curve(p0, p1, p2, p3, steps=20):
    M = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])

    Gx = np.array([p0[0], p1[0], p2[0], p3[0]], dtype=float)
    Gy = np.array([p0[1], p1[1], p2[1], p3[1]], dtype=float)

    Cx = M.dot(Gx)
    Cy = M.dot(Gy)

    for i in range(steps + 1):
        t = i / steps if steps > 0 else 0.0
        T = np.array([t**3, t**2, t, 1.0])
        x: float = float(T.dot(Cx))
        y: float = float(T.dot(Cy))
        yield (round(x), round(y), 1.0)


def bspline_curve(points, steps=20):
    if len(points) < 4:
        return

    M = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]]) / 6.0

    for seg in range(len(points) - 3):
        p0, p1, p2, p3 = points[seg], points[seg + 1], points[seg + 2], points[seg + 3]

        Gx = np.array([p0[0], p1[0], p2[0], p3[0]], dtype=float)
        Gy = np.array([p0[1], p1[1], p2[1], p3[1]], dtype=float)

        Cx = M.dot(Gx)
        Cy = M.dot(Gy)

        for i in range(steps + 1):
            t = i / steps if steps > 0 else 0.0
            T = np.array([t**3, t**2, t, 1.0])
            x: float = float(T.dot(Cx))
            y: float = float(T.dot(Cy))
            yield (round(x), round(y), 1.0)
