def matrix_mult(a, b):
    if len(a[0]) != len(b):
        raise ValueError("Matrix dimensions don't match for multiplication")

    result = [[0] * len(b[0]) for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]
    return result


def matrix_vector_mult(matrix, vector):
    result = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(vector)):
            result[i] += matrix[i][j] * vector[j]
    return result


def hermite_curve(p0, p1, m0, m1, steps=20):
    h00 = lambda t: 2 * t**3 - 3 * t**2 + 1
    h10 = lambda t: t**3 - 2 * t**2 + t
    h01 = lambda t: -2 * t**3 + 3 * t**2
    h11 = lambda t: t**3 - t**2

    for i in range(steps + 1):
        t = i / steps if steps > 0 else 0

        x = h00(t) * p0[0] + h10(t) * m0[0] + h01(t) * p1[0] + h11(t) * m1[0]
        y = h00(t) * p0[1] + h10(t) * m0[1] + h01(t) * p1[1] + h11(t) * m1[1]

        yield (round(x), round(y), 1.0)


def bezier_curve(p0, p1, p2, p3, steps=20):
    for i in range(steps + 1):
        t = i / steps if steps > 0 else 0
        mt = 1 - t

        b0 = mt**3
        b1 = 3 * mt**2 * t
        b2 = 3 * mt * t**2
        b3 = t**3

        x = b0 * p0[0] + b1 * p1[0] + b2 * p2[0] + b3 * p3[0]
        y = b0 * p0[1] + b1 * p1[1] + b2 * p2[1] + b3 * p3[1]

        yield (round(x), round(y), 1.0)


def bspline_curve(points, steps=20):
    if len(points) < 4:
        return

    for segment_idx in range(len(points) - 3):
        p0 = points[segment_idx]
        p1 = points[segment_idx + 1]
        p2 = points[segment_idx + 2]
        p3 = points[segment_idx + 3]

        for i in range(steps + 1):
            t = i / steps if steps > 0 else 0
            mt = 1 - t

            n0 = mt**3 / 6
            n1 = (3 * t**3 - 6 * t**2 + 4) / 6
            n2 = (-3 * t**3 + 3 * t**2 + 3 * t + 1) / 6
            n3 = t**3 / 6

            x = n0 * p0[0] + n1 * p1[0] + n2 * p2[0] + n3 * p3[0]
            y = n0 * p0[1] + n1 * p1[1] + n2 * p2[1] + n3 * p3[1]

            yield (round(x), round(y), 1.0)
