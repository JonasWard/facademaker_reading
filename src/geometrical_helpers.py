import Rhino.Geometry as rg
import math
from debugging_tools import list_counter

def pts_min_height(pts):
    """function that finds the minimum height of a list of rg.Point3ds
    return:
    height: float"""
    zs=[]
    for pt in pts:
        zs.append(pt.Z)

    return min(zs)
    
def ptss_min_height(ptss):
    """function that finds the minimum height of a list of a list of rg.Point3ds
    return:
    height: float"""
    return min([pts_min_height(pts) for pts in ptss])

def ptsss_min_height(ptsss):
    """function that finds the minimum height of a list of a list of a list of 
    rg.Point3ds
    return:
    height: float"""

    return min([ptss_min_height(ptss) for ptss in ptsss])

def pt_increase(pt, value):
    pt.Z+=value

def pts_increase(pts, value):
    [pt_increase(pt, value) for pt in pts]

def ptss_increase(ptss, value):
    [pts_increase(pts, value) for pts in ptss]

def ptsss_increase(ptsss, value):
    [ptss_increase(ptss, value) for ptss in ptsss]

def fix_pt_height(pt, treshold_height):
    """function that tries to check whether the z value of a rg.Point3ds is
    larger than a given treshold value, if not, all the points z'height are
    increased until it reaches the treshold value"""

    min_h=pt.Z

    if min_h<treshold_height:
        h_delta=treshold_height-min_h
        print("treshold height was not reached, height was increased by {}".format(h_delta) )
        pt_increase(pt, h_delta)
    
def fix_pts_heights(pts, treshold_height):
    """function that tries to check whether the z value of a list of rg.Point3ds 
    are larger than a given treshold value, if not, all the points z'height are
    increased until it reaches the treshold value"""

    min_h=pts_min_height(pts)

    if min_h<treshold_height:
        h_delta=treshold_height-min_h
        print("treshold height was not reached, heights were increased by {}".format(h_delta) )
        pts_increase(pts, h_delta)

def fix_ptss_heights(ptss, treshold_height):
    """function that tries to check whether the z value of a list of rg.Point3ds 
    lists are larger than a given treshold value, if not, all the points 
    z'height are increased until it reaches the treshold value"""

    # print(list_counter(ptss))
    min_h=ptss_min_height(ptss)

    if min_h<treshold_height:
        h_delta=treshold_height-min_h
        print("treshold height was not reached, heights were increased by {}".format(h_delta) )
        ptss_increase(ptss, h_delta)

def fix_ptsss_heights(ptsss, treshold_height):
    """function that tries to check whether the z value of a list of rg.Point3ds 
    lists are larger than a given treshold value, if not, all the points 
    z'height are increased until it reaches the treshold value"""

    # print(list_counter(ptss))
    min_h=ptsss_min_height(ptsss)

    if min_h<treshold_height:
        h_delta=treshold_height-min_h
        print("treshold height was not reached, heights were increased by {}".format(h_delta) )
        ptsss_increase(ptsss, h_delta)

def tangent_normal(pt_0, pt_1, negative=False):
    t=rg.Vector3d(pt_1-pt_0)
    t.Unitize()
    if negative:
        n=rg.Vector3d(-t.Y, t.X, 0.0)
    else:
        n=rg.Vector3d(t.Y, -t.X, 0.0)
    return t, n

def create_half_circle(pt, r, t, n):
    pt_a=rg.Point3d(pt - rg.Point3d(t * r) )
    pt_b=rg.Point3d(pt + rg.Point3d(n * r) )
    pt_c=rg.Point3d(pt + rg.Point3d(t * r) )
    arc_crv=rg.ArcCurve(rg.Arc(pt_a, pt_b, pt_c) )
    return arc_crv

def triangulate(pt_0, pt_1, dis_0, dis_1, negative=False):
    t, n = tangent_normal(pt_0, pt_1, negative)

    crv_0=create_half_circle(pt_0, dis_0, t, n)
    crv_1=create_half_circle(pt_1, dis_1, t, n)

    i_s=rg.Intersect.Intersection.CurveCurve(crv_0, crv_1, 0.001, 0.0)
    final_pt=i_s[0].PointA
    # print(final_pt)
    return final_pt

def bounds(pts):
    """function that gives you the min and max x,y coordinates of a set of points"""
    xs, ys = [], []
    for pt in pts:
        xs.append(pt.X)
        ys.append(pt.Y)

    return (min(xs), min(ys)), (max(xs), max(ys))

def bounding_rec(pts, angle=None):
    """iterative function for calculating the bounding box of a given set of points"""
    if angle is None:
        (x_min, y_min), (x_max, y_max) = bounds(pts)
        return rg.Point3d(x_min, y_min, 0.0), x_max-x_min, y_max-y_min

    else:
        r_tm=rg.Transform.Rotation(angle, rg.Point3d(0,0,0) )   # initializing a rotation matrix
        loc_pts=[rg.Point3d(pt) for pt in pts]                  # initializing a copy
        [pt.Transform(r_tm) for pt in loc_pts]                  # transforming the copied points
        return bounding_rec(loc_pts)

def optimal_rec(pts, iterations=50, max_width=10000.0, max_height=10000.0):
    delta=.5*math.pi/(iterations - 1)

    data_dict={}
    for i in range(iterations):
        # duplicate pts
        loc_pts=[rg.Point3d(pt) for pt in pts]
        angle=i*delta
        _, w, l=bounding_rec(loc_pts, angle)
        if w < max_width and l < max_height:
            data_dict[angle]={"width":w,"length":l,"area":w*l}

    angle_dict={}
    if any(data_dict):
        angle_dict["width"]=min(data_dict, key=lambda k: data_dict[k]["width"])
        angle_dict["length"]=min(data_dict, key=lambda k: data_dict[k]["length"])
        angle_dict["area"]=min(data_dict, key=lambda k: data_dict[k]["area"])
    else:
        print("trying to optimize this object, the constrains were reached")

    return angle_dict

def transform_objs(objs, t_m):
    [obj.Transform(t_m) for obj in objs]

def centroid(pts):
    centroid=rg.Point3d(pts[1])
    for pt in pts[1:]:
        centroid+=pt

    centroid*=1.0/float(len(pts) )
    return rg.Point3d(centroid)