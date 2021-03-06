# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
import numpy as np


def region_growing(image,coordinate,number):
    """Give coordinate and size,return a region."""
    # tmp_image store marks and rg_image store new image after region grow
    nt = number
    tmp_image = np.zeros_like(image)
    rg_image = np.zeros_like(image)
    image_shape = image.shape

    x = coordinate[0]
    y = coordinate[1]
    z = coordinate[2]

    # ensure the coordinate is in the image
    inside = (x >= 0) and (x < image_shape[0]) and (y >= 0) and \
             (y < image_shape[1]) and (z >= 0) and (z < image_shape[2])
    if inside != True:
        print "The coordinate is out of the image range."
        return False

    # initialize region_mean and region_size
    region_mean = image[x, y, z]
    region_size = 0

    # initialize neighbor_list with 10000 rows 4 columns
    neighbor_free = 10000
    neighbor_pos = -1
    neighbor_list = np.zeros((neighbor_free, 4))

    # 26 direct neighbor points
    neighbors  = [[1,0,0], \
                  [-1,0,0], \
                  [0,1,0], \
                  [0,-1,0], \
                  [0,0,-1], \
                  [0,0,1], \
                  [1,1,0], \
                  [1,1,1], \
                  [1,1,-1], \
                  [0,1,1], \
                  [-1,1,1], \
                  [1,0,1], \
                  [1,-1,1], \
                  [-1,-1,0], \
                  [-1,-1,-1], \
                  [-1,-1,1], \
                  [0,-1,-1], \
                  [1,-1,-1], \
                  [-1,0,-1], \
                  [-1,1,-1], \
                  [0,1,-1], \
                  [0,-1,1], \
                  [1,0,-1], \
                  [1,-1,0], \
                  [-1,0,1], \
                  [-1,1,0]]

    while region_size < nt:
        # (xn, yn, zn) store direct neighbor of seed point
        for i in range(6):
            xn = x + neighbors[i][0]
            yn = y + neighbors[i][1]
            zn = z + neighbors[i][2]

            # ensure the coordinate is in the image
            inside = (xn >= 0) and (xn < image_shape[0]) and (yn >= 0) and \
                     (yn < image_shape[1]) and (zn >= 0) and (zn < image_shape[2])

            # ensure the original flag 0 is not changed
            if inside and tmp_image[xn, yn, zn]==0:
                # add this point to neighbor_list and mark it with 1
                neighbor_pos = neighbor_pos + 1
                neighbor_list[neighbor_pos] = [xn, yn, zn, image[xn, yn, zn]]
                tmp_image[xn, yn, zn] = 1

        # ensure there is enough space to store neighbor_list
        if (neighbor_pos+100 > neighbor_free):
            neighbor_free += 10000
            new_list = np.zeros((10000, 4))
            neighbor_list = np.vstack((neighbor_list, new_list))

        # the distance between every neighbor point value to new region mean value
        distance = np.abs(neighbor_list[:neighbor_pos+1, 3] - np.tile(region_mean, neighbor_pos+1))

        # chose the min distance point
        #voxel_distance = distance.min()
        index = distance.argmin()

        # mark the new region point with 2 and update new image
        tmp_image[x, y, z] = 2
        rg_image[x, y, z] = image[x, y, z]
        region_size += 1

        # (x, y, z) the new seed point
        x = neighbor_list[index][0]
        y = neighbor_list[index][1]
        z = neighbor_list[index][2]

        # update region mean value
        region_mean = (region_mean*region_size+neighbor_list[index, 3])/(region_size+1)

        # remove the seed point from neighbor_list
        neighbor_list[index] = neighbor_list[neighbor_pos]
        neighbor_pos -= 1

    return rg_image
