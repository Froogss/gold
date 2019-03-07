import io

import numpy
from PIL import Image


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)


def perspective_change(image, new_coords):
    width, height = image.size
    # top ,right, bottom, left
    base_coords = [[0, 0], [width, 0], [width, height], [0, height]]
    # new_coords = [[-width*0.3,0], [width*1.3,0],[width,height],[0,height]]

    res = find_coeffs(base_coords, new_coords)

    return image.transform((width, height), Image.PERSPECTIVE, res, Image.BICUBIC)
