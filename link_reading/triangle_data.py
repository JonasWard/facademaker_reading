class TriangleData:
    def __init__(self, l, w, hs, rel_top_shift = 0.0, is_up = True):
        self.l = l
        self.w = w
        self.hs = hs # 00, 10, 11

        self.ls = rel_top_shift

        if not( len(hs) == 3 ) :
            raise ValueError("only takes 3 inputs for heights, given {}".format(len(hs)))

        self._is_up = is_up

    def clone(self):
        return TriangleData(self.l, self.w, self.hs, self.ls, self._is_up)

    def rotate(self, count):
        tmp_hs = [ self.hs[ (i + count) % 3 ] for i in range(3) ]
        self.hs = tmp_hs

    def flip_h(self):
        tmp_hs = [ self.hs[i] for i in [1, 0, 2] ]
        self.hs = tmp_hs

    def flip_v(self):
        self._is_up = not(self._is_up)

    def get_pts(self):
        if self._is_up:
            b_pts = [
                (0, 0, self.hs[0]),
                (self.l, 0, self.hs[1]),
                (self.l * (self.ls + .5), self.w, self.hs[2])
            ]
        
        else:
            b_pts = [
                (0, self.w, self.hs[0]),
                (self.l * (self.ls + .5), 0, self.hs[2]),
                (0, self.w, self.hs[1])
            ]
        
        return b_pts