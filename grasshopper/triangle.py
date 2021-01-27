from complex_pt_handling import Simple, Center, optimal_rec
from baking import bake
import Rhino.Geometry as rg

class Triangle:
    def __init__(self, pts, correction, side_interlock, mesh_correction = False, extra_folds = False):
        self.datastructure = Simple(pts, 0)
        
        if mesh_correction:
            self.datastructure.mesh_correction(correction)
        else:
            if abs(correction) > .01:
                self.datastructure.polyline_correction(correction)

        self._interlockicking(side_interlock)
        self._unfolded = False
        self._extra_folds = extra_folds

    def _interlockicking(self, interlock_type):
        self.pattern = [(0,0)]
        
        if interlock_type==0:
            self.pattern = [(0,0)]

        elif interlock_type==1:
            self.pattern = [(1,1)]
            
        elif interlock_type==2:
            self.pattern = [(2,2)]
            
        elif interlock_type==3:
            self.pattern = [(3,1),(1,3)]

        elif interlock_type==4:
            self.pattern = [(1,3),(3,1)]

        elif interlock_type==5:
            self.pattern = [3]

    def mesh(self, show_with_correction_val = 0.0):
        return self.datastructure.rhino_mesh(show_with_correction_val)

    def unfolded(self, h_max = 30.0, position_optimization = {"iterations" : 100, "max_w" : 800., "max_l" : 1800., "preference" : "area"}, b_pt=rg.Point3d.Origin ):
        self.datastructure.unfolding()
        outline_pts, main_folds, inner_folds = self.datastructure.add_complex_sides(h_max=h_max, pattern=self.pattern)
        outline = rg.PolylineCurve(outline_pts)
        secundary_folds = self._folds() if self._extra_folds else []

        w_angle, l_angle, area_angle, _ = optimal_rec(
            outline_pts,
            position_optimization["iterations"],
            position_optimization["max_w"],
            position_optimization["max_l"]
        )
        
        if position_optimization["preference"] == "width":
            angle = w_angle
        elif position_optimization["preference"] == "length":
            angle = l_angle
        else:
            angle = area_angle

        rot_matrix=rg.Transform.Rotation(angle, rg.Point3d(0,0,0) )
        trans_matrix=rg.Transform.Translation(rg.Vector3d(b_pt) )

        to_transform=[main_folds,[outline],secundary_folds,inner_folds]
        cleaned_objs=[]
        for obj_list in to_transform:
            loc_obj_list=[]
            for obj in obj_list:
                if not(obj is None):
                    loc_obj_list.append(obj)
            cleaned_objs.append(loc_obj_list)

        # transforming everying in one swoop, the objects remain the same anyway
        x, y, z, u=tuple(cleaned_objs)
        to_transform=x+y+z+u
        [obj.Transform(rot_matrix) for obj in to_transform]
        [obj.Transform(trans_matrix) for obj in to_transform]

        self.outline, self.main_folds, self.secundary_folds, self.inner_folds = outline, main_folds, secundary_folds, inner_folds
        self._unfolded = True
        return outline, main_folds, secundary_folds, inner_folds
    
    def _folds(self):
        return self.datastructure.fold_lns()

    def bake(self):
        if not(self._unfolded):
            self.unfolded()

        return {
            "outline":[self.outline],
            "main_folds":self.main_folds,
            "sec_folds":self.secundary_folds,
            "inner_folds":self.inner_folds
        }

class CenterTriangle(Triangle):
    def __init__(self, b_pts, c_pt, correction, side_interlock, mesh_correction = False, extra_folds = False):
        self.datastructure = Center(b_pts, c_pt, 0)

        if mesh_correction:
            self.datastructure.mesh_correction(correction)
        else:
            if abs(correction) > .01:
                self.datastructure.polyline_correction(correction)

        self._interlockicking(side_interlock)
        self._unfolded = False
        self._extra_folds = extra_folds