class SquareData:
    def __init__(self, l, w, hs, ls = 0.0, b_pt = None):
        self.l = l
        self.w = w
        self.hs = hs # 00, 10, 11, 01
        self.ls = ls

        if not( len(hs) == 4 ) :
            raise ValueError("only takes 4 inputs for heights, given {}".format(len(hs)))
        
        self._b_shift = True # True = bottom, False = top
        self._has_center = False
        self._in_out = False

        self.b_pt = b_pt
        self._has_base = not(self.b_pt is None)

    def add_center(self, a, b, h_in, h_out):
        self._has_center = True

        self.a = a
        self.b = b
        self.h_in = h_in
        self.h_out = h_out

    def clone(self):
        new_square = SquareData(self.l, self.w, self.hs, self.ls)
        if self._has_center:
            new_square.add_center(self.a, self.b, self.h_in, self.h_out)

        return new_square

    def rotate(self, count):
        tmp_hs = [ self.hs[ (i + count) % 4 ] for i in range(4) ]
        self.hs = tmp_hs

        if self._has_center:
            self.a, self.b = [
                (self.a, self.b),
                (1 - self.a, self.b),
                (1 - self.a, 1 - self.b),
                (self.a, 1 - self.b)
            ][count % 4]

    def flip_h(self):
        tmp_hs = [ self.hs[i] for i in [3, 2, 1, 0] ]
        self.hs = tmp_hs

        if self._has_center:
            self.b = 1.0 - self.b

    def flip_v(self):
        tmp_hs = [ self.hs[i] for i in [1, 0, 3, 2] ]
        self.hs = tmp_hs

        self._b_shift = not(self._b_shift)

        if self._has_center:
            self.a = 1.0 - self.a

    def flip_in_out(self):
        self._in_out = not(self._in_out)

    def create_corner_points(self):
        corner_pts = [
            [ 0, 0, self.hs[0] ],
            [ self.l, 0, self.hs[1] ],
            [ self.l, self.w, self.hs[2] ],
            [ 0, self.w, self.hs[3] ]
        ]

        if self._has_base:
            for c_pt in corner_pts:
                c_pt[0] += self.b_pt[0]
                c_pt[1] += self.b_pt[1]

        return corner_pts

    @property
    def center_point(self):
        center_pt = [
            self.a * self.l,
            self.b * self.w,
            [self.h_in, self.h_out][self._in_out]
        ]

        if self._has_base:
            center_pt[0] += self.b_pt[0]
            center_pt[1] += self.b_pt[1]

        return center_pt
    
    def get_pts(self):
        b_pts = self.create_corner_points()
        
        # apply shift
        if self._b_shift:
            b_pts[0][0] += self.ls
            b_pts[1][0] += self.ls
        else:
            b_pts[2][0] += self.ls
            b_pts[3][0] += self.ls

        if self._in_out and not(self._has_center): # order switch for square type
            b_pts = b_pts[1:] + [ b_pts[0] ]

        if self._has_center:
            return b_pts, self.center_point
        else:
            return b_pts

    def split(self, with_center = False):
        if not(self._has_center):
            print("had to initialize a,b values, cause not present ...")
            self.a = .5
            self.b = .5

        ### will right now only work double subdivision ###
        ws = [self.b * self.w, (1.0 - self.b) * self.w]
        y_bases = [0.0, self.b * self.w]

        ls = [self.a * self.l, (1.0 - self.a) * self.l]
        x_bases = [0.0, self.a * self.l]

        hs_remap = [
            [self.hs[0], self.hs[1]],
            [self.hs[3], self.hs[2]]
        ]

        new_squares = []

        for j in range(2):
            w = ws[j]             
            y_base = y_bases[j]

            for i in range(2):
                l = ls[i]
                x_base = x_bases[i]

                loc_hs = [hs_remap[j][i] for i in range(4)]

                new_squares.append( SquareData(l, w, loc_hs, [x_base, y_base] ) )