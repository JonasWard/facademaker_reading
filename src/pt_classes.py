from Rhino.Geometry import Point3d

class PtSet:
    """class that does pt set generation for FrontEndSet objects"""
    def __init__(self):
        self.set_b_p()
        self.pt_cnt=4

    def set_b_p(self):
        """method that sets some initial parameters"""

        self._rot=0
        self._hkon=False
        self._vkon=False
        self._hmir=False
        self._vmir=False

        self._base_fold_idx=1

    def rotate(self, value):
        self._rot+=value
        self._rot%=self.pt_cnt

    def h_mir(self):
        self._hmir=not(self._hmir)

    def v_mir(self):
        self._vmir=not(self._vmir)

    def h_kon(self):
        self._hkon=not(self._hkon)

    def v_kon(self):
        self._vkon=not(self._vkon)

    def __repr__(self):
        return """{} class with:
        \t-pt_cnt:{}
        \t-h_kon: {}
        \t-v_kon: {}
        \t-h_mir: {}
        \t-v_mir: {}
        \t-rot:   {}""".format(
            self.__class__.__name__,
            self.pt_cnt,
            self._hkon,
            self._vkon,
            self._hmir,
            self._vmir,
            self._rot
        )

class SquarePts(PtSet):
    def __init__(self, x, y, hs, s):
        self.pt_cnt=4
        self.set_b_p()

        self.x=x
        self.y=y
        self.s=s

        self.hs=hs

    def gen_base_pts(self):
        b_set=[
            Point3d(0., 0., 0.),
            Point3d(self.x, 0., 0.),
            Point3d(self.x, self.y, 0.),
            Point3d(0., self.y, 0.),
        ]

        if self._vmir:
            b_set[0].X+=self.s
            b_set[1].X+=self.s
        else:
            b_set[2].X+=self.s
            b_set[3].X+=self.s

        return b_set
    
    def switch_heights(self):
        print("switching heights")
        if self._rot!=0:
            self.hs=self.hs[self._rot:]+self.hs[:self._rot]
        
        if self._hmir:
            self.hs=[self.hs[i] for i in [1, 0, 3, 2]]

        if self._vmir:
            self.hs=[self.hs[i] for i in [3, 2, 1, 0]]

    @property
    def fold_idx(self):
        f_idx=self._base_fold_idx
        f_idx+=self._rot
        f_idx+=int(self._hmir)
        f_idx+=int(self._vmir)
        f_idx+=int(self._hkon)
        f_idx+=int(self._vkon)
        print("unmodulated f_idx: {}, %2 f_idx: {}".format(f_idx, f_idx%2) )
        return f_idx%2

    def generate(self):
        print(self)
        b_pts=self.gen_base_pts()
        self.switch_heights()
        for i, b_pt in enumerate(b_pts):
            b_pt.Z=self.hs[i]

        # b_pts=b_pts[self.fold_idx:]+b_pts[:self.fold_idx]

        return [b_pts]

class TrianglePts(PtSet):
    def __init__(self, x, y, hs, s):
        self.pt_cnt=4
        self.set_b_p()

        self.x=x
        self.y=y
        self.s=s

        self.hs=hs

    def h_kon(self):
        self._hkon=False

    def v_kon(self):
        self._vkon=False

    def switch_heights(self):
        if self._hmir^self._vmir:
            pass
        else:
            self.hs=[self.hs[i] for i in [0, 2, 1]]

        if self._rot!=0:
            self.hs=self.hs[self._rot:]+self.hs[:self._rot]

    def has_ortogonal_angle(self):
        return abs(self.s)<.001

    def gen_base_pts(self):
        if (
            not(self._vmir^self._hmir) and self.has_ortogonal_angle() or 
            (self._vmir and not(self.has_ortogonal_angle()))
        ):
            b_set=[
                [
                    Point3d(0., self.y, 0.),
                    Point3d(self.s, 0., 0.),
                    Point3d(self.x, self.y, 0.)
                ],[
                    Point3d(self.x+self.s, 0., 0.),
                    Point3d(self.x, self.y, 0.),
                    Point3d(self.s, 0., 0.)
                ]
            ]
        else:
            b_set=[
                [
                    Point3d(0., 0., 0.),
                    Point3d(self.x, 0., 0.),
                    Point3d(self.s, self.y, 0.)
                ],[
                    Point3d(self.s+self.x, self.y, 0.),
                    Point3d(self.s, self.y, 0.),
                    Point3d(self.x, 0., 0.)
                ]
            ]

        return b_set

    def generate(self):
        print(self)
        b_ptss=self.gen_base_pts()
        self.switch_heights()
        for b_pts in b_ptss:
            for i, b_pt in enumerate(b_pts):
                b_pt.Z=self.hs[i]

        return b_ptss

class HenningTriangles(TrianglePts):
    def __init__(self, x, y, hs, s):
        self.pt_cnt=4
        self.set_b_p()

        self.x=x
        self.y=y
        self.s=s

        self.hs=hs
        self.dir=1.0

    def h_kon(self):
        self._hkon=False

    def v_kon(self):
        self._vkon=False

    def switch_heights(self):
        if self._hmir^self._vmir:
            pass
        else:
            self.hs=[self.hs[i] for i in [0, 2, 1]]

        if self._rot!=0:
            self.hs=self.hs[self._rot:]+self.hs[:self._rot]

    def gen_base_pts(self):
        if self._vmir:
            b_set=[
                [
                    Point3d(0., 0., 0.),
                    Point3d(self.x, 0., 0.),
                    Point3d(self.s, self.y, 0.)
                ],[
                    Point3d(self.s+self.x, self.y, 0.),
                    Point3d(self.s, self.y, 0.),
                    Point3d(self.x, 0., 0.)
                ]
            ]
        else:
            b_set=[
                [
                    Point3d(0., self.y, 0.),
                    Point3d(self.s, 0., 0.),
                    Point3d(self.x, self.y, 0.)
                ],[
                    Point3d(self.x+self.s, 0., 0.),
                    Point3d(self.x, self.y, 0.),
                    Point3d(self.s, 0., 0.)
                ]
            ]

        return b_set

class PyramidPts(SquarePts):
    def __init__(self, x, y, hs, a, b, hc, s):
        self.pt_cnt=4
        self.set_b_p()

        self.x=x
        self.y=y
        self.s=s

        self.hs=hs

        self.a=a
        self.b=b
        self.hc=hc

    def h_kon(self):
        self._hkon=False

    def v_kon(self):
        self._vkon=False

    def manage_ab(self):
        """method to transform a & b"""
        if self._rot==1:
            self.a=1.-self.a
        elif self._rot==2:
            self.a=1.-self.a
            self.b=1.-self.b
        elif self._rot==3:
            self.b=1.-self.b

        if self._vmir:
            self.b=1.-self.b

        if self._hmir:
            self.a=1.-self.a

    @property
    def x_vec(self):
        return Point3d(self.x, 0., 0.)

    @property
    def y_vec(self):
        s=-self.s if self._vmir else self.s
        return Point3d(s, self.y, 0.)

    def gen_c_pt(self):
        """method to retrieve c_pt"""
        self.manage_ab()
        pt=self.a*self.x_vec+self.b*self.y_vec
        pt.Z=self.hc

        return pt

class DiamondPts(SquarePts):
    def __init__(self, x, y, hs, s=0.):
        self.pt_cnt=4
        self.set_b_p()

        self.x=x
        self.y=y
        self.s=s

        self._bt=False

        self.hs=hs

    def index_input(self, idx):
        self._bt=(idx%2==1)

    def gen_base_pts(self):
        b_set=[
            Point3d(-self.x*.5, 0., 0.),
            Point3d(0., -self.y, 0.),
            Point3d(self.x*.5, 0., 0.),
            Point3d(0., self.y, 0.),
        ]

        if self._bt:
            for pt in b_set:
                pt.X-=self.x*.5

        return b_set
    
    def switch_heights(self):
        print("switching heights")
        if self._rot!=0:
            self.hs=self.hs[self._rot:]+self.hs[:self._rot]
        
        if self._hmir:
            self.hs=[self.hs[i] for i in [1, 0, 3, 2]]

        if self._vmir:
            self.hs=[self.hs[i] for i in [3, 2, 1, 0]]

class QuadGroupPts(PyramidPts):
    def __init__(self, x, y, hs, a, b, s):
        self.pt_cnt=4
        self.set_b_p()

        self.x=x
        self.y=y
        self.s=s

        self.hs=hs

        self.a=a
        self.b=b

    def _row_function(self, b_pt, pos_a, pos_b):
        row=[]
        for i,j in [(0.,0.),(pos_a,0.),(pos_a,pos_b),(0.,pos_b)]:
            row.append(b_pt+i*self.x_vec+j*self.y_vec)
        return row

    def gen_base_pts(self):
        if self._vmir:
            b_pt=Point3d(self.s, 0., 0.)
        else:
            b_pt=Point3d(0., 0., 0.)

        self.manage_ab()

        b_ptsss=[]
        b_pt_00=b_pt
        b_ptsss.append(self._row_function(b_pt_00,self.a,self.b) )

        b_pt_01=b_pt+self.a*self.x_vec
        b_ptsss.append(self._row_function(b_pt_01,1.-self.a,self.b) )

        b_pt_11=b_pt+self.a*self.x_vec+self.b*self.y_vec
        b_ptsss.append(self._row_function(b_pt_11,1.-self.a,1.-self.b) )

        b_pt_10=b_pt+self.b*self.y_vec
        b_ptsss.append(self._row_function(b_pt_10,self.a,1.-self.b) )

        return b_ptsss

    def generate(self):
        # print(self)
        b_ptss=self.gen_base_pts()
        self.switch_heights()
        for i, b_pts in enumerate(b_ptss):
            for b_pt in b_pts:
                b_pt.Z=self.hs[i]

        return b_ptss