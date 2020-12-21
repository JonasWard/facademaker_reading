class Square:
    def __init__(self, l, w, hs):
        self.l = l
        self.w = w
        self.hs = hs # 00, 10, 11, 01

        if not( len(hs) == 4 ) :
            raise ValueError("only takes 4 inputs for heights, given {}".format(len(hs)))

        self._has_center = False
        self._in_out = False

    def add_center(self, a, b, h_in, h_out):
        self._has_center = True

        self.a = a
        self.b = b
        self.h_in = h_in
        self.h_out = h_out

    def rotate(self, count):
        tmp_hs = [ self.hs[ (i + count) % 4 ] for i in range(4) ]
        self.hs = tmp_hs

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

        if self._has_center:
            self.a = 1.0 - self.a

    def flip_in_out(self):
        self._in_out = not(self._in_out)

    
    def get_pts(self):
        b_pts = [ ( 0, 0, self.hs[0] ), ( self.l, 0, self.hs[1] ), ( self.l, self.w, self.hs[2] ), ( 0, self.w, self.hs[3] ) ]
        
        if self._in_out and not(self._has_center):
            b_pts = b_pts[1:] + [ b_pts[0] ]

        if self._has_center:
            return b_pts, (self.a * self.l, self.b * self.w, [self.h_in, self.h_out][self._in_out])
        else:
            return b_pts

    

