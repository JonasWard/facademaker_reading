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

    def fold_idx(self):
        #TODO write based on henning code
        return 0

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
        if self._rot!=0:
            self.hs=self.hs[self._rot:]+self.hs[:self._rot]
        
        if self._hmir:
            self.hs=[self.hs[i] for i in [1, 0, 3, 2]]

        if self._vmir:
            self.hs=[self.hs[i] for i in [3, 2, 1, 0]]

    @property
    def fold_idx(self):
        #TODO write based on henning code
        return 0

    def generate(self):
        b_pts=self.gen_base_pts()
        for i, b_pt in enumerate(b_pts):
            b_pt.Z=self.hs[i]
        return [b_pts]

class TrianglePts(PtSet):
    def __init__(self, x, y, hs, s):
        self.pt_cnt=4
        self.set_b_p()

        self.x=x
        self.y=y
        self.s=s

        self.hs=hs

    def switch_heights(self):
        if self._rot!=0:
            self.hs=self.hs[self._rot:]+self.hs[:self._rot]

        if self._hmir^self._vmir:
            pass
        else:
            self.hs=[self.hs[i] for i in [0, 2, 1]]

    def gen_base_pts(self):
        if self._vmir^self._hmir:
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
                    Point3d(self.x+self.s, self.y, 0.)
                ],[
                    Point3d(self.x+self.s, 0., 0.),
                    Point3d(self.x, self.y, 0.),
                    Point3d(self.s, 0., 0.)
                ]
            ]

        return b_set

    @property
    def fold_idx(self):
        return 0

    def generate(self):
        b_ptss=self.gen_base_pts()
        for b_pts in b_ptss:
            for i, b_pt in enumerate(b_pts):
                b_pt.Z=self.hs[i]
        return b_ptss

class DiamondPts(PtSet):
    def __init__(self, x, y, hs, a, b, s):
        pass