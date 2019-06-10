import math
import numpy
import sympy
import mpmath
from sympy import symbols, Eq, solve, nsolve
from sympy.geometry import Ray, Circle, intersection

def get_distance_from_rssi(measured_power, rssi):
    n = 2
    distance = math.pow(10, (measured_power - rssi) / (10 * n))
    return distance

if __name__ == '__main__' :

    rssi_remi = int(input("RSSI Remi:\n"))
    rssi_fred = int(input("RSSI Fred:\n"))
    rssi_quentin = int(input("RSSI Quentin:\n"))

    Tx_remi = -30
    Tx_fred = -30
    Tx_quentin = -30

    posX_remi = -2.5
    posY_remi = 2.5

    posX_fred = 2.5
    posY_fred = -2.5

    posX_quentin = -2.5
    posY_quentin = -2.5

    distance_remi = get_distance_from_rssi(Tx_remi, rssi_remi)
    print("Distance AP Remi : " + str(distance_remi) + " m")

    distance_fred = get_distance_from_rssi(Tx_fred, rssi_fred)
    print("Distance AP Fred : " + str(distance_fred) + " m")

    distance_quentin = get_distance_from_rssi(Tx_quentin, rssi_quentin)
    print("Distance AP Quentin : " + str(distance_quentin) + " m")

    # remi → (x+2.5)² + (y+2.5)² = distance_remi
    # fred → (x-2.5)² + (y-2.5)² = distance_fred
    # quentin → (x+2.5)² + (y-2.5)² = distance_remi

    # Définition des cercles
    c_remi = sympy.geometry.Circle((posX_remi, posY_remi), distance_remi)
    c_fred = sympy.geometry.Circle((posX_fred, posY_fred), distance_fred)
    c_quentin = sympy.geometry.Circle((posX_quentin, posY_quentin), distance_quentin)

    # Définition des intersections des cercles
    intersect_remi_fred_1 = intersection(c_remi, c_fred)[0]
    intersect_remi_fred_2 = intersection(c_remi, c_fred)[1]
    intersect_remi_quentin_1 = intersection(c_remi, c_quentin)[0]
    intersect_remi_quentin_2 = intersection(c_remi, c_quentin)[1]
    intersect_fred_quentin_1 = intersection(c_fred, c_quentin)[0]
    intersect_fred_quentin_2 = intersection(c_fred, c_quentin)[1]

    # Définition des coordonnées des intersections des cercles
    remi_fred_1_x = float(intersect_remi_fred_1[0])
    remi_fred_1_y = float(intersect_remi_fred_1[1])
    remi_fred_2_x = float(intersect_remi_fred_2[0])
    remi_fred_2_y = float(intersect_remi_fred_2[1])
    remi_quentin_1_x = float(intersect_remi_quentin_1[0])
    remi_quentin_1_y = float(intersect_remi_quentin_1[1])
    remi_quentin_2_x = float(intersect_remi_quentin_2[0])
    remi_quentin_2_y = float(intersect_remi_quentin_2[1])
    fred_quentin_1_x = float(intersect_fred_quentin_1[0])
    fred_quentin_1_y = float(intersect_fred_quentin_1[1])
    fred_quentin_2_x = float(intersect_fred_quentin_2[0])
    fred_quentin_2_y = float(intersect_fred_quentin_2[1])

    # Sélection des intersections significatives
    if remi_fred_1_y < remi_fred_2_y:
        remi_fred_x = remi_fred_1_x
        remi_fred_y = remi_fred_1_y
    else:
        remi_fred_x = remi_fred_2_x
        remi_fred_y = remi_fred_2_y

    if remi_quentin_1_x**2 + remi_quentin_1_y**2 < remi_quentin_2_x**2 + remi_quentin_2_y**2:
        remi_quentin_x = remi_quentin_1_x
        remi_quentin_y = remi_quentin_1_y
    else:
        remi_quentin_x = remi_quentin_2_x
        remi_quentin_y =remi_quentin_2_y

    if fred_quentin_1_x**2 + fred_quentin_1_y**2 < fred_quentin_2_x**2 + fred_quentin_2_y**2:
        fred_quentin_x = fred_quentin_1_x
        fred_quentin_y = fred_quentin_1_y
    else:
        fred_quentin_x = fred_quentin_2_x
        fred_quentin_y = fred_quentin_2_y

    print("\nIntersection remi_fred: " + str(remi_fred_x) + ',' + str(remi_fred_y))
    print("Intersection remi_quentin: " + str(remi_quentin_x) + ',' + str(remi_quentin_y))
    print("Intersection fred_quentin: " + str(fred_quentin_x) + ',' + str(fred_quentin_y))

    # Construction d'un polygone à partir des coordonnées d'intersection
    triangle = sympy.Polygon(
        sympy.Point2D(remi_fred_x, remi_fred_y),
        sympy.Point2D(remi_quentin_x, remi_quentin_y),
        sympy.Point2D(fred_quentin_x, fred_quentin_y))

    # Calcul de l'isobarycentre du polygone
    antoine_x = float(triangle.centroid[0])
    antoine_y = float(triangle.centroid[1])

    # Calcul de l'aire du polygone
    triangle_surfaceArea = float(triangle.area)

    print("\nCoordonnées mesurées: " + str(antoine_x) + ',' + str(antoine_y))
    print("Surface possible autour de ce point: " + str(triangle_surfaceArea) + " m²")