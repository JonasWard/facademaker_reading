class Polygon:
    HCOUNT = 4
    def __init__(self, l, w, hs, shift, b_pt = (0,0) ):
        self.l = l
        self.w = w
        self.hs = hs

        self.check_valid_hs(self)
        
        self.ls = shift
        self.b_ppt = b_pt

        self._has_center = False

    def check_valid_hs(self):
        class_h_count = type(self).HCOUNT
        given_h_count = len(self.hs)
        if not(given_h_count == class_h_count):
            print("""an invalid amount of height values have been given {} 
            while you need {}, your data has been adjusted to fit.""".format(
                given_h_count, class_h_count) )

            self.hs = [self.hs[i % given_h_count] for i in range(class_h_count)]

    def add_center(self, a, b, h_in, h_out):
        self._has_center = True

        self.a = a
        self.b = b
        self.h_in = h_in
        self.h_out = h_out

    def clone(self):
        new_polygon = type(self).__class__(self.l, self.w, self.hs, self.ls, self.b_pt)
        if self._has_center:
            new_polygon.add_center(self.a, self.b, self.h_in, self.h_out)

        return new_polygon

    def _b_corner_f(self):
        # as if it were a square
        
        corner_pts = [
            [ 0, 0, self.hs[0] ],
            [ self.l, 0, self.hs[1] ],
            [ self.l, self.w, self.hs[2] ],
            [ 0, self.w, self.hs[3] ]
        ]

    def corner_points(self):
        corner_pts = self._b_corner_f(self)

        for c_pt in corner_pts:
            c_pt[0] += self.b_pt[0]
            c_pt[1] += self.b_pt[1]

        return corner_pts

