import Rhino.Geometry as rg
from geometrical_helpers import *

class PanelSideSegment():
    """ PanelSideSegment class, defined by two points ( a line ) two definitions:
        - defined using orignal pts and new unfolded given: simple_side, complex_side
        - defined using only the new unfolded given: simple_flap, portrusion"""
    def __init__(self, pt_0, pt_1):
        self.pt_0=pt_0
        self.pt_1=pt_1

    @property
    def t(self):
        _t=rg.Vector3d(self.pt_1-self.pt_0)
        _t.Unitize()

        return _t

    @property 
    def n(self):
        return rg.Vector3d(-self.t.Y, self.t.X, 0.0)

    @property
    def dis00(self):
        return self.pt_0.Z

    @property
    def dis01(self):
        return self.pt_0.DistanceTo(rg.Point3d(self.pt_1.X, self.pt_1.Y, 0.0) )

    @property
    def dis10(self):
        return self.pt_1.DistanceTo(rg.Point3d(self.pt_0.X, self.pt_0.Y, 0.0) )

    @property
    def dis11(self):
        return self.pt_1.Z

    @property
    def dis(self):
        return self.pt_0.DistanceTo(self.pt_1)

    def simple_side(self, pt_0, pt_1):
        """pattern logic that just create a flat (projected) side for this segment"""
        pt_0_1=triangulate(pt_0, pt_1, self.dis00, self.dis10, True)
        pt_1_1=triangulate(pt_0, pt_1, self.dis01, self.dis11, True)

        return [pt_0_1, pt_1_1], [rg.Line(pt_0, pt_1)]

    def complex_side(self, pt_0, pt_1, h_max, pattern_type=["straight","straight"] ):
        new_pts, fold_a=self.simple_side(pt_0, pt_1)

        n_s_0=PanelSideSegment(new_pts[0], pt_0)
        n_s_1=PanelSideSegment(new_pts[1], pt_1)

        seg_pts=[]
        folds_b=[]

        # n_s_0
        loc_folds_b=[]
        if pattern_type[0]=="straight":
            loc_seg_pts=[new_pts[0] ]
        elif pattern_type[0]=="positive":
            loc_seg_pts, _=n_s_0.portrusion(h_max, False)
        elif pattern_type[0]=="negative":
            loc_seg_pts, loc_folds_b=n_s_0.portrusion(h_max, True)
        else:
            print("this pattern type '{}' is not defined".format(pattern_type[0]))

        loc_seg_pts.reverse()
        seg_pts.extend(loc_seg_pts)
        folds_b.extend(loc_folds_b)

        # n_s_1
        loc_folds_b=[]
        if pattern_type[1]=="straight":
            loc_seg_pts=[new_pts[1] ]
        elif pattern_type[1]=="positive":
            loc_seg_pts, loc_folds_b = n_s_1.portrusion(h_max, False)
        elif pattern_type[1]=="negative":
            loc_seg_pts, _ = n_s_1.portrusion(h_max, True)
        else:
            print("this pattern type '{}' is not defined".format(pattern_type[1]))

        seg_pts.extend(loc_seg_pts)
        folds_b.extend(loc_folds_b)

        return seg_pts, fold_a, folds_b

    def simple_flap(self, h, w, invert=False):
        iv=-1.0 if invert else 1.0

        # mv=rg.Point3d(iv*self.t*w + self.n*h)
        new_pts=[
            self.pt_0+rg.Point3d(iv*self.t*w + self.n*h),
            self.pt_1+rg.Point3d(-iv*self.t*w + self.n*h)
        ]

        fold_lines=[rg.Line(self.pt_0, self.pt_1)]

        return new_pts, fold_lines

    def portrusion(self, h_max, direction):
        # print("creating a portrusion")
        t, n = tangent_normal(self.pt_0, self.pt_1)
        dir_val=1.0 if direction else -1.0

        h=self.dis
        if h < h_max:
            pt_s=[self.pt_0+dir_val*n*h]
        else:
            pt_s=[
                self.pt_0+dir_val*n*h_max,
                self.pt_0+dir_val*n*h_max+t*(h-h_max)
            ]

        return pt_s, [rg.Line(self.pt_0, self.pt_1)]