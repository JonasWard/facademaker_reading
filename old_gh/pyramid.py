from complex_pt_handling import Center, optimal_rec
from baking import bake
import Rhino.Geometry as rg
from triangle import Triangle, CenterTriangle

class Pyramid:
    def __init__(self, b_pts, c_pt, correction, side_interlock, split_idx = 0, mesh_correction = False, extra_folds = False):
        self.triangle = Triangle([b_pts[0], c_pt, b_pts[-1] ], correction, side_interlock, mesh_correction, extra_folds)
        self.square = CenterTriangle(b_pts, c_pt, correction, side_interlock, mesh_correction = False, extra_folds = False)

        self.triangle.flap_interlocking(side_interlock)

    def mesh(self, show_with_correction_val = 0.0):
        return [self.square.mesh(show_with_correction_val), self.triangle.mesh(show_with_correction_val)]

    def unfolded(self, h_max = 30.0, position_optimization = {"iterations" : 100, "max_w" : 800., "max_l" : 1800., "preference" : "area"}, b_pt=rg.Point3d.Origin ):
        outline, main_folds, secundary_folds, inner_folds = [], [], [], []
        
        for i, shp in enumerate([self.square, self.triangle]):
            if i == 1:
                b_pt = rg.Point3d(max( position_optimization["max_w"], position_optimization["max_l"] ) + 200., 0, 0)
            
            x, y, z, u = shp.unfolded(h_max = 30.0, position_optimization = {"iterations" : 100, "max_w" : 800., "max_l" : 1800., "preference" : "area"}, b_pt = b_pt)

            outline.append(x)
            main_folds.extend(y)
            secundary_folds.extend(z)
            inner_folds.extend(u)

        return outline, main_folds, secundary_folds, inner_folds

    def bake(self):
        a_dict = {}
        for i, shp in enumerate([self.square, self.triangle]):
            for key, values in shp.bake().items():
                if i == 0:
                    a_dict[key] = values
                else:
                    a_dict[key].extend(values)

        return a_dict