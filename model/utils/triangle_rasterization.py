# Use real division everywhere
from __future__ import division

import numpy as np


def rasterize_triangle(tri):
    """
    Given a 3x2 numpy array TRI describing the integer vertices of a general
    triangle, return an array containing all the points that lie within this
    triangle or on the triangle's edge, but not the triangle vertices
    themselves.
    """
    # Sort by increasing y coordinate
    tri = tri[tri[:, 1].argsort()]

    # Check for triangles with horizontal edge
    if tri[1, 1] == tri[2, 1]:
        # Bottom is horizontal
        points = rasterize_flat_triangle(tri)
    elif tri[0, 1] == tri[1, 1]:
        # Top is horizontal
        points = rasterize_flat_triangle(tri[(2, 0, 1), :])
    else:
        # General triangle.
        # We'll split this into two triangles with horizontal edges and process
        # them separately.
        # Find the additional vertex that splits the triangle.
        helper_point = np.array([tri[0, 0] + (tri[1, 1] - tri[0, 1]) /
                                         (tri[2, 1] - tri[0, 1]) *
                                         (tri[2, 0] - tri[0, 0]),
                                         tri[1, 1]]).round()
        # Top triangle
        points = rasterize_flat_triangle(tri[(0, 1), :],
            helper_point=helper_point)
        # Bottom triangle
        points = np.vstack([points, rasterize_flat_triangle(tri[(2, 1), :],
            helper_point=helper_point)])

    return points


def rasterize_flat_triangle(tri, helper_point=None):
    '''
    Given a 3x2 numpy array TRI describing the vertices of a triangle where the
    second and third vertex have the same y coordinate, return an array
    containing all the points that lie within this triangle or
    on the triangle's edge, but not the triangle vertices themselves.
    Or, given a 2x2 numpy array TRI containing two vertices and HELPER_POINT
    containing the third vertex, again return the same points as before, but
    additionally return the helper_point as well (used when treating a
    general triangle that's split into two triangles with horizontal edges)
    '''
    # Is the triangle we're treating part of a split triangle?
    if helper_point is not None:
        tri = np.vstack([tri, helper_point])

    # Is the bottom or the top edge horizontal?
    ydir = np.sign(tri[1, 1] - tri[0, 1])

    # Make sure that the horizontal edge is left-right oriented
    if tri[1, 0] > tri[2, 0]:
        tri[1, 0], tri[2, 0] = tri[2, 0], tri[1, 0]

    # Find the inverse slope (dx/dy) for the two non-horizontal edges
    invslope1 = ydir * (tri[1, 0] - tri[0, 0]) / (tri[1, 1] - tri[0, 1])
    invslope2 = ydir * (tri[2, 0] - tri[0, 0]) / (tri[2, 1] - tri[0, 1])

    # Initialize the first scan line, which is one y-step below or above the
    # first vertex
    curx1 = tri[0, 0] + invslope1
    curx2 = tri[0, 0] + invslope2
    points = []

    # Step vertically. Don't include the first row, because that row only
    # contains the first vertex and we don't want to return the vertices
    for y in np.arange(tri[0, 1] + ydir, tri[1, 1], ydir):
        for x in np.arange(curx1.round(), curx2.round() + 1):
            points.extend([(x, y)])
        curx1 += invslope1
        curx2 += invslope2

    # If we're dealing with the first half of a split triangle, add the
    # helper point (because that's not a "real" vertex of the triangle)
    if helper_point is not None and ydir == 1:
        points.extend([tuple(helper_point)])

    # If we're not dealing with a split triangle, or if we're dealing with the
    # first half of a split triangle, add the last line (but without the end
    # points, because they're the vertices of the triangle
    if helper_point is None or ydir == 1:
        for x in np.arange(tri[1, 0] + 1, tri[2, 0]):
            points.extend([(x, tri[1, 1])])

    return np.array(points, dtype='int')