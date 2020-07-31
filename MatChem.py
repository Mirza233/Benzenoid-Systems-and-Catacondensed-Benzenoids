#!/usr/bin/env python3

import math
import matplotlib.pyplot as plt  # Used only for drawing

"""
Suppose that the infinite hexagonal lattice is equipped with
a coordinate system. Any benzenoid system can be represented
as a list of hexagons, e.g. [(1, 2), (1, 3), (2, 2)]. 
"""

def to_canonical_trans(b):
    """
    Transform the benzenoid system so that all coordinates are
    non-negative integers and as small as possible.
    Example: [(1, 2), (1, 3), (2, 2)] -> [(0, 0), (0, 1), (1, 0)]
    """
    i_min = min(i for (i, j) in b)
    j_min = min(j for (i, j) in b)
    return sorted([(i - i_min, j - j_min) for (i, j) in b])

def rotation_60(b):
    """
    Rotate the benzenoid system by 60 degrees in the counter-clockwise
    direction.
    """
    return [(i + j, -i) for (i, j) in b]

def reflection(b):
    """
    Reflect the benzenoid system over a line.
    """
    return [(-i, i + j) for (i, j) in b]

def to_canonical(b):
    """
    Return the canonical form of a benzenoid system b. All symmetries
    of benzenoid systems are taken into account.
    """
    l = [to_canonical_trans(b)]
    r = [to_canonical_trans(reflection(b))]
    for i in range(5):
        l.append(to_canonical_trans(rotation_60(l[-1])))
        r.append(to_canonical_trans(rotation_60(r[-1])))
    return tuple(min(min(l), min(r)))

def are_isomorphic(b1, b2):
    """
    Return True if benzenoid system b1 and b2 are isomorphic.
    """
    return sorted(to_canonical(b1)) == sorted(to_canonical(b2))

def neighbours(h):
    """
    Return the list of neighbours of a hexagon h = (i, j).
    """
    i, j = h
    return [(i + 1, j), (i + 1, j - 1), (i, j - 1),
            (i - 1, j), (i - 1, j + 1), (i, j + 1)]

def layer_of_fat(b):
    """
    Return the list of all hexagons that are adjacent to some
    hexagon of b, but do not belong to b.
    """
    f = set()
    for h in b:
        for n in neighbours(h):
            if n not in b:
                f.add(n)
    return list(f)

def list_of_benzenoids(h):
    """
    Return the list of all benzenoid system with h hexagons.
    All benzenoids are in the canonical form.
    """
    l = [((0, 0),)]  # Benzene

    for i in range(h - 1):
        l_new = set()
        for b in l:
            f = layer_of_fat(b)
            for hexagon in f:
                l_new.add(to_canonical(b + (hexagon,)))
        l = sorted(list(l_new))
    return l

def get_vertices(h):
    """
    Return the coordinates of vertices of a hexagon.
    """
    i, j = h
    vertices = [(math.sqrt(3) / 2, 1 / 2), (0, 1), (-math.sqrt(3) / 2, 1 / 2),
               (-math.sqrt(3) / 2, -1 / 2), (0, -1), (math.sqrt(3) / 2, -1 / 2)]
    x_centre, y_centre = math.sqrt(3) * j + math.sqrt(3) / 2 * i, 3 / 2 * i
    
    return [x_centre + x for x, _ in vertices], [y_centre + y for _, y in vertices]

def draw_benzenoid(b, file_name):
    """
    Draw the benzenoid system b and save the image to the file
    named file_name.
    """
    fig = plt.figure()
    plt.axis('equal')
    for h in b:
        x_list, y_list = get_vertices(h)
        plt.fill(x_list, y_list, facecolor='lightsalmon', edgecolor='orangered', linewidth=2)
    fig.savefig(file_name)
    plt.close(fig)


##################################################################################################
    
def get_vertices1(h):
    v = get_vertices(h)
    return [(v[0][i],v[1][i]) for i in range(6)]
    

        
def get_vertices_system(b):
    vertices = []
    for h in b:
        vertices+=[i for i in get_vertices1(h)]
    return set(map(lambda x:(round(x[0],3),round(x[1],3)),vertices))

def get_edges(h):
    x,y = get_vertices(h)
    edges = []
    for i in range(6):
        edges.append(tuple(sorted([(round(x[i-1],3),round(y[i-1],3)),(round(x[i],3),round(y[i],3))])))
    return list(set(edges))

def get_edges_system(b):
    edges = []
    for h in b:
        edges+=get_edges(h)
    return set(edges)


        
def is_coronoid(b):
    n = len(get_vertices_system(b))
    m = len(get_edges_system(b))
    h = len(b)
    #print(n,m,h)
    return m >= n+h  #If the system is indeed coronoid, the equality holds, strict inequality holds if there are >=2 "holes".


def benzenoids(n):
    l = list_of_benzenoids(h)
    l = list(filter(lambda x:not is_coronoid(x),l))
    return l


    
def is_catacondensed(b):
    if len(b) <=2:
        return True
    n = len(b)
    return len(get_vertices_system(b)) == 6*n-2*(n-1)


def list_of_catacondensed(h):
    return list(filter(is_catacondensed,benzenoids(h)))
                
def draw_catacondensed(h):
    l = benzenoids(h)
    count = 0
    for i in l:
        if is_catacondensed(i):
            count+=1
            draw_benzenoid(i,"Benzenoid "+str(count))

def catacondensed_filter(b):
    for h in b:
        i,j = h
        if ((i,j+1) in b) and ((i+1,j) in b): return False
        elif ((i+1,j) in b) and ((i+1,j-1) in b): return False
    return True

def VE(h):
    X,Y = get_vertices(h)
    V = []
    for i in range(6): V.append((X[i],Y[i]))
    E = []
    for i in range(6): E.append((V[i-1],V[i]))
    return V,E

def filter_list(l):
    l1 = []
    l = set(l)
    for i in l:
        if (i[1],i[0]) in l:
            continue
        l1.append(i)
    return l1

def VE(h):
    X,Y = get_vertices(h)
    V = []
    for i in range(6): V.append((X[i],Y[i]))
    E = []
    for i in range(6): E.append({V[i],V[i-1]})
    SV = set()
    SE = set()
    for i in range(6):
        SV.add(V[i])
        SE.add(frozenset(E[i]))
    return (SV,SE)
        

def benzenoid_filter(b):
    V = set()
    E = set()
    for h in b:
        Vh, Eh = VE(h)
        V.update(Vh)
        E.update(Eh)
    print(len(E),len(V))
    if len(V)+len(b) <= len(E): return True
    else: return False


if __name__ == '__main__':
    h = int(input())
    l1 = benzenoids(h)
    """"""
    l = list_of_benzenoids(h)
    l = list(filter(lambda x: benzenoid_filter(x),l))
    """"""
    #l_cat =  list(filter(lambda x: is_catacondensed(x),l))
    #l_cat = list_of_catacondensed(h)
    l_cat = list(filter(catacondensed_filter,benzenoids(h)))
    print('Number of benzenoid systems on {0} hexagons: {1}'.format(h, len(l)))
    print(len(l1))
    print('The list of all benzenoid systems:')

    for i, b in enumerate(l):
        break #Comment this line to get the list and to draw all benzenoids
        print("{0:4d}  {1}".format(i + 1, b))
        draw_benzenoid(b, 'benzenoid_{0}_{1:02d}.png'.format(h, i + 1))
    print('Number of benzenoid catacondensed systems on {0} hexagons: {1}'.format(h, len(l_cat)))
    print('The list of all benzenoid systems:')
    for i, b in enumerate(l_cat):
        break  #Comment this line to get the list and to draw all catacondensed benzenoids
        print("{0:4d}  {1}".format(i + 1, b))
        draw_benzenoid(b, 'benzenoid_{0}_{1:02d}.png'.format(h, i + 1))
