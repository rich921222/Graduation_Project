import numpy as np

def NearestPoint():
    def distance_from_origin(point):
        x, y = point
        return x**2 + y**2
    points = []
    for x in range(-16, 17):
        for y in range(-16, 17):
                points.append((x, y)) 
    points.sort(key=distance_from_origin) 

    return np.array(points)