from pt_classes import TrianglePts, SquarePts, PyramidPts, DiamondPts, QuadGroupPts

class FrontEndSet:
    """class that contains all the genral functions to opperate on all the
    front end objects"""
    def __init__(self):
        self.set_b_p()
        self.pt_cnt=4

    def set_b_p(self, hs=[]):
        """method that sets some initial parameters and also deals with the
        height setting"""
        if (len(hs)==0):
            self.hs=[0. for i in range(self.pt_cnt)]
        else:
            self.hs=[hs[i%len(hs)] for i in range(self.pt_cnt)]

        self._hrot=0
        self._vrot=0
        self._hkon=False
        self._vkon=False
        self._hmir=False
        self._vmir=False

    @property
    def is_complex(self):
        self.b_oss=[[]]

        return (
            self._hrot!=0 or
            self._vrot!=0 or
            self._hkon or
            self._vkon or
            self._hmir or
            self._vmir
        )

    @property
    def has_v(self):
        return self._vrot!=0 or self._vmir or self._vkon

    @property
    def has_h(self):
        return self._hrot!=0 or self._hmir or self._hkon

    @property
    def corner_copy(self):
        if self.has_h and self.has_v:
            return (
                ((self._vrot+self._hrot)%4==0) and
                (self._hkon==self._vkon) and
                (self._hmir==self._vmir)
            )
        else:
            return False

    def h_rot(self, value):
        self._hrot+=value
        self._hrot%=self.pt_cnt

    def v_rot(self, value):
        self._vrot+=value
        self._vrot%=self.pt_cnt

    def h_mir(self):
        self._hmir=not(self._hmir)

    def v_mir(self):
        self._vmir=not(self._vmir)

    def h_kon(self):
        self._hkon=not(self._hkon)

    def v_kon(self):
        self._vkon=not(self._vkon)

    def populate(self):
        return None

    def apply_all_transformations(self):
        if self.has_h:
            for b_os in self.b_oss:
                for i in range(1, len(b_os), 2):
                    if self._hmir:
                        b_os[i].h_mir()
                    if self._hkon:
                        b_os[i].h_kon()
                    if self._hrot!=0:
                        b_os[i].rotate(self._hrot)

        if self.has_v:
            for i in range(1, len(self.b_oss), 2):
                for b_o in self.b_oss[i]:
                    if self._vmir:
                        b_o.v_mir()
                    if self._vkon:
                        b_o.v_kon()
                    if self._vrot!=0:
                        b_o.rotate(self._vrot)

    def generate_b_pts(self):
        """method that sets the base_objects, stores them and returns their base_ptsss"""
        if self.has_v:
            self.b_oss=[[],[]]
        else:
            self.b_oss=[[]]

        if self.has_h:
            for b_os in self.b_oss:
                for _ in range(2):
                    b_os.append(self.populate())
        else:
            for b_os in self.b_oss:
                b_os.append(self.populate())

        self.apply_all_transformations()

        pt_sets=[]
        for b_os in self.b_oss:
            row=[]
            for b_o in b_os:
                row.extend(b_o.generate())
            pt_sets.append(row)

        return pt_sets

    def generate(self):
        return self.generate_b_pts()

    def fold_idxs(self):
        """method that gives you the fold idxs of all the elements in this object
        requires you to have called generate() before"""
        fold_idxs=[]

        for b_os in self.b_oss:
            row=[]
            for b_o in b_os:
                row.append(b_o.fold_idx)
            fold_idxs.append(row)

        return fold_idxs

    def flat_clone(self, height=0.):
        clone_pt_sets=self.generate()
        for ptss in clone_pt_sets:
            for pts in ptss:
                for pt in pts:
                    pt.Z=height

        return clone_pt_sets

class TriangleSet(FrontEndSet):
    """class that allows you to manage triangle objects. Either this class
    should have 1x2 pt sets as an output, or it will have 2x4. hkon and vkon
    parameters don't have an effect on this type."""
    def __init__(self, x, y, hs, s=0.0, ss=None):
        """input:
        x:  float - height of the projected triangle
        y:  float - width of the projected triangle
        hs: list of floats - heights of the points (should have length 3, outfits otherwise)
        s:  float (default 0.0) - value indicating how much you shift the top point relative to the width
        ss: (optional) float (default: None) - if not none, will override s, and use a static shift for the top point"""

        self.pt_cnt=3

        self.set_b_p(hs)
        self.x=x
        self.y=y
        
        self.s=s*x
        if not(ss is None):
            self.s=ss

    def h_kon(self):
        print("tried to change concavity/fold idx but this is not defined for the triangle class")
        self._hkon=False

    def v_kon(self):
        print("tried to change concavity/fold idx but this is not defined for the triangle class")
        self._vkon=False

    def _gen_triangle(self):
        return TrianglePts(self.x, self.y, self.hs, s=self.s)

    def populate(self):
        return self._gen_triangle()

class SquareSet(FrontEndSet):
    """class that allows you to manage triangle objects. Either this class
    should have 1x1 pt sets as an output, or it will have 2x2, quad group
    and pyramid are derivatives of this one."""
    def __init__(self, x, y, hs, s=0.0, ss=None):
        """input:
        x:  float - height of the projected triangle
        y:  float - width of the projected triangle
        hs: list of floats - heights of the points (should have length 4, outfits otherwise)
        s:  float (default 0.0) - value indicating how much you shift the top point relative to the width
        ss: (optional) float (default: None) - if not none, will override s, and use a static shift for the top point"""

        self.pt_cnt=4

        self.set_b_p(hs)
        self.x=x
        self.y=y
        self.s=s*x
        if not(ss is None):
            self.s=ss

    def _gen_square(self):
        return SquarePts(self.x, self.y, self.hs, s=self.s)

    def populate(self):
        return self._gen_square()

class PyramidSet(FrontEndSet):
    """class that allows you to manage pyramid objects. Either this class
    should have 1x1 pt sets as an output, or it will have 2x2"""
    def __init__(self, x, y, hs, a=.5, b=.5, hc=0., s=0., ss=None):
        """input:
        x:  float - height of the projected square
        y:  float - width of the projected square
        hs: list of floats - heights of the points (should have length 4, outfits otherwise)
        a:  float (default 0.5) - relative position x-vector
        b:  float (default 0.5) - relative position y-vector
        hc: float (default 0.0) - height of the center coordinate
        s:  float (default 0.0) - value indicating how much you shift the top point relative to the width
        ss: (optional) float (default: None) - if not none, will override s, and use a static shift for the top point"""

        self.pt_cnt=4

        self.set_b_p(hs)
        self.x=x
        self.y=y

        self.a=a
        self.b=b
        self.hc=hc

        self.s=s*x
        if not(ss is None):
            self.s=ss

    def _gen_pyramid(self):
        return PyramidPts(self.x, self.y, self.hs, self.a, self.b, self.hc, self.s)

    def populate(self):
        return self._gen_pyramid()

    def get_c_ptss(self):
        """method that gives you the center points of all the elements in this object"""
        c_ptss=[]

        for b_os in self.b_oss:
            row=[]
            for b_o in b_os:
                row.append(b_o.gen_c_pt())
            c_ptss.append(row)

        return c_ptss

    def generate(self):
        ptsss=self.generate_b_pts()

        shifted_ptsss=[]
        for ptss in ptsss:
            row=[]
            for pts in ptss:
                pts=pts[1:]+pts[:1]
            row.append(pts)
        shifted_ptsss.append(row)

        return shifted_ptsss

class DiamondSet(FrontEndSet):
    """class that allows you to manage diamond objects. Either this class
    should have 1x1 pt sets as an output, or it will have 2x2"""
    def __init__(self, x, y, hs, s=0., ss=None):
        """input:
        x:  float - height of the projected diamond
        y:  float - width of the projected diamond
        hs: list of floats - heights of the points (should have length 4, outfits otherwise)
        s:  float (default 0.0) - value indicating how much you shift the top point relative to the width
        ss: (optional) float (default: None) - if not none, will override s, and use a static shift for the top point"""

        self.pt_cnt=4

        self.set_b_p(hs)
        self.x=x
        self.y=y

        self.s=s*x
        if not(ss is None):
            self.s=ss

    def _gen_diamond(self):
        return DiamondPts(self.x, self.y, self.hs, self.s)

    def generate_b_pts(self):
        """method that sets the base_objects, stores them and returns their base_ptsss"""
        self.b_oss=[[],[]]

        if self.has_h:
            for b_os in self.b_oss:
                for _ in range(2):
                    b_os.append(self.populate())
        else:
            for b_os in self.b_oss:
                b_os.append(self.populate())

        self.apply_all_transformations()

        pt_sets=[]
        for i, b_os in enumerate(self.b_oss):
            row=[]
            for b_o in b_os:
                b_o.index_input(i)
                row.extend(b_o.generate())
            pt_sets.append(row)

        return pt_sets

    def populate(self):
        return self._gen_diamond()

class QuadGroupSet(FrontEndSet):
    """class that allows you to manage pyramid objects. Either this class
    should have 1x1 pt sets as an output, or it will have 2x2"""
    def __init__(self, x, y, hs, a=.5, b=.5, s=0., ss=None):
        """input:
        x:  float - height of the projected square
        y:  float - width of the projected square
        hs: list of floats - heights of the points (should have length 4, outfits otherwise)
        a:  float (default 0.5) - relative position x-vector
        b:  float (default 0.5) - relative position y-vector
        s:  float (default 0.0) - value indicating how much you shift the top point relative to the width
        ss: (optional) float (default: None) - if not none, will override s, and use a static shift for the top point"""

        self.pt_cnt=4

        self.set_b_p(hs)
        self.x=x
        self.y=y

        self.a=a
        self.b=b

        self.s=s*x
        if not(ss is None):
            self.s=ss

    def _gen_quad_group(self):
        return QuadGroupPts(self.x, self.y, self.hs, self.a, self.b, self.s)

    def populate(self):
        return self._gen_quad_group()

    def generate_b_pts(self):
        """method that sets the base_objects, stores them and returns their base_ptsss"""
        if self.has_v:
            self.b_oss=[[],[]]
        else:
            self.b_oss=[[]]

        # initializing all the objects
        if self.has_h:
            for b_os in self.b_oss:
                for _ in range(2):
                    b_os.append(self.populate())
        else:
            for b_os in self.b_oss:
                b_os.append(self.populate())

        # applying the correct transformations to all the objects
        self.apply_all_transformations()

        # generating the correct point lists
        pt_sets=[]
        for b_os in self.b_oss:
            row=[]
            for b_o in b_os:
                row.append(b_o.generate())
            pt_sets.append(row)

        # print("FES.generate_b_pts")

        return pt_sets

    def generate(self):
        ptssss=self.generate_b_pts()

        return ptssss

