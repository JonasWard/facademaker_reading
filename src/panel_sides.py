import Rhino.Geometry as rg
from geometrical_helpers import *
from math import tan

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

    def complex_side(self, pt_0, pt_1, data_dict, pattern_type=["straight","straight"] ):
        new_pts, fold_a=self.simple_side(pt_0, pt_1)

        n_s_0=PanelSideSegment(new_pts[0], pt_0)
        n_s_1=PanelSideSegment(new_pts[1], pt_1)

        seg_pts=[]
        folds_b=[]
        holes=[]

        extra_pt=False
        # n_s_0
        loc_seg_pts=[]
        loc_folds_b=[]
        loc_holes=[]

        if pattern_type[0]=="straight":
            loc_seg_pts=[new_pts[0] ]
        elif pattern_type[0]=="positive":
            loc_seg_pts, _=n_s_0.portrusion(data_dict, False)
        elif pattern_type[0]=="negative":
            loc_seg_pts, loc_folds_b=n_s_0.portrusion(data_dict, True)
        elif pattern_type[0]=="easyfix_pos":
            loc_seg_pts, _, loc_holes=n_s_0.easy_fix_portrusion(data_dict, False)
        elif pattern_type[0]=="easyfix_neg":
            loc_seg_pts, loc_folds_b, loc_holes=n_s_0.easy_fix_portrusion(data_dict, True)
            extra_pt=True
        elif pattern_type[0]=="easyfix_pos_simple":
            loc_seg_pts, _, loc_holes=n_s_0.triangle_end(data_dict, False)
        elif pattern_type[0]=="easyfix_neg_simple":
            loc_seg_pts, loc_folds_b, loc_holes=n_s_0.triangle_end(data_dict, True)
            extra_pt=True
        else:
            print("this pattern type '{}' is not defined".format(pattern_type[0]))

        if extra_pt:
            print("adding an extra_pt")
            loc_seg_pts=[n_s_0.pt_0]+loc_seg_pts

        holes.extend(loc_holes)

        # point to be added in case easy fix
        pt_f_0=loc_seg_pts[0]

        loc_seg_pts.reverse()
        seg_pts.extend(loc_seg_pts)
        folds_b.extend(loc_folds_b)

        extra_pt=False
        # n_s_1
        loc_seg_pts=[]
        loc_folds_b=[]
        loc_holes=[]

        if pattern_type[1]=="straight":
            loc_seg_pts=[new_pts[1] ]
        elif pattern_type[1]=="positive":
            loc_seg_pts, loc_folds_b = n_s_1.portrusion(data_dict, False)
        elif pattern_type[1]=="negative":
            loc_seg_pts, _ = n_s_1.portrusion(data_dict, True)
        elif pattern_type[1]=="easyfix_pos":
            loc_seg_pts, loc_folds_b, loc_holes=n_s_1.easy_fix_portrusion(data_dict, False)
            extra_pt=True
        elif pattern_type[1]=="easyfix_neg":
            loc_seg_pts, _, loc_holes=n_s_1.easy_fix_portrusion(data_dict, True)
        elif pattern_type[1]=="easyfix_pos_simple":
            loc_seg_pts, loc_folds_b, loc_holes=n_s_1.triangle_end(data_dict, False)
            extra_pt=True
        elif pattern_type[1]=="easyfix_neg_simple":
            loc_seg_pts, _, loc_holes=n_s_1.triangle_end(data_dict, True)
        else:
            print("this pattern type '{}' is not defined".format(pattern_type[1]))

        if extra_pt:
            loc_seg_pts=[n_s_1.pt_0]+loc_seg_pts

        holes.extend(loc_holes)

        # point to be added in case easy fix
        pt_f_1=loc_seg_pts[0]

        if (
                (pattern_type[0]=="easyfix_pos" or pattern_type[0]=="easyfix_neg") or
                (pattern_type[0]=="easyfix_pos_simple" or pattern_type[0]=="easyfix_neg_simple")
            ):

            loc_f_seg_pts, loc_f_folds_b = PanelSideSegment(pt_f_0, pt_f_1).simple_flap(data_dict)
            seg_pts.extend(loc_f_seg_pts)
            folds_b.extend(loc_f_folds_b)

        seg_pts.extend(loc_seg_pts)
        folds_b.extend(loc_folds_b)

        return seg_pts, fold_a, folds_b

    def triangle_end(self, data_dict, direction=False):
        print("triangle end portrusion")
        angle = data_dict["side_angle"]

        cot=1./tan(angle)
        t, n = tangent_normal(self.pt_0, self.pt_1)
        dir_val=cot if direction else -cot

        holes=[]

        pt_s=[self.pt_0+dir_val*n*self.dis]

        return pt_s, [rg.Line(self.pt_0, self.pt_1)], holes

    def simple_flap(self, data_dict, invert=False):
        print("simple flap")

        h, w = data_dict["flap_h"], data_dict["flap_w"]
        iv=-1.0 if invert else 1.0

        new_pts=[
            self.pt_0+rg.Point3d(iv*self.t*w + self.n*h),
            self.pt_1+rg.Point3d(-iv*self.t*w + self.n*h)
        ]

        fold_lines=[rg.Line(self.pt_0, self.pt_1)]

        return new_pts, fold_lines

    def portrusion(self, data_dict, direction):
        print("simple end portrusion")
        h_max = data_dict["flap_h_max"]

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

    def easy_fix_portrusion(self, data_dict, direction):
        print("easy_fix end portrusion")

        h_lid, l, angle = data_dict["flap_h_max"], data_dict["flap_l_max"], data_dict["side_angle"]
        cot=1./tan(angle)
        t, n = tangent_normal(self.pt_0, self.pt_1)
        dir_val=cot if direction else -cot

        holes=[]

        if self.dis*cot < h_lid or self.dis*cot > l:
            print("tried to add an easy fix end, but reached treshold states")
            print("cot: {}, dis: {}, dis*cot: {}, h_lid: {}, l: {}, l*cot:{}".format(cot, self.dis, self.dis*cot, h_lid, l, l*cot))
            pt_s=[self.pt_0+dir_val*n*self.dis]
        else:
            pt_s=[
                self.pt_0+dir_val*n*l,
                self.pt_0+dir_val*n*l+t*h_lid,
                self.pt_0+dir_val*n*(self.dis-h_lid)+t*h_lid
            ]

        return pt_s, [rg.Line(self.pt_0, self.pt_1)], holes

