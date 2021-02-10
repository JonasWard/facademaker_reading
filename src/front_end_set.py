from pt_classes import TrianglePts, SquarePts, DiamondPts

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

    def apply_all_transformations(self, b_oss):
        if self.has_h:
            for b_os in b_oss:
                for i in range(1, len(b_os), 2):
                    if self._hmir:
                        b_os[i].h_mir()
                    if self._hkon:
                        b_os[i].h_kon()
                    if self._hrot!=0:
                        b_os[i].rotate(self._hrot)

        if self.has_v:
            for i in range(1, len(b_oss), 2):
                for b_o in b_oss[i]:
                    if self._vmir:
                        b_o.v_mir()
                    if self._vkon:
                        b_o.v_kon()
                    if self._vrot!=0:
                        b_o.rotate(self._vrot)

    def generate(self):
        """method that sets the base_objects and then transforms them into base_ptsss"""
        if self.has_v:
            b_oss=[[],[]]
        else:
            b_oss=[[]]

        if self.has_h:
            for b_os in b_oss:
                for _ in range(2):
                    b_os.append(self.populate())
        else:
            for b_os in b_oss:
                b_os.append(self.populate())

        self.apply_all_transformations(b_oss)

        pt_sets=[]
        for b_os in b_oss:
            row=[]
            for b_o in b_os:
                row.extend(b_o.generate())
            pt_sets.append(row)

        return pt_sets

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

class DiamondSet(FrontEndSet):
    """class that allows you to manage diamond objects. Either this class
    should have 1x1 pt sets as an output, or it will have 2x2"""
    def __init__(self, x, y, hs, a=.5, b=.5, s=0.0, ss=None):
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

        self.a=a
        self.b=b

        self.s=s*x
        if not(ss is None):
            self.s=ss

    def duplicate(self):
        return DiamondPts(self.x, self.y, self.hs, self.a, self.b, s=self.s)