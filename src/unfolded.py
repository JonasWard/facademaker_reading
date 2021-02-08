import Rhino.Geometry as rg
from geometrical_helpers import optimal_rec, centroid, bounds

class Unfolded():
    """container class for the unfolded objects,
        - used to check whether they fit on a sheet
        - moving the objects around as a single group"""
    DEFAULT_SHEET_PARAMETERS={
        "h":1800.,
        "w":1000.
    }
    
    def __init__(self, boundary, top_face_folds=[], body_flap_folds=[], intra_flap_folds=[], sheet_parameters=None):
        self.b_pts=boundary
        self.f_ff=top_face_folds
        self.f_bf=body_flap_folds
        self.f_if=intra_flap_folds

        if sheet_parameters is None:
            self.s_para = dict(Unfolded.DEFAULT_SHEET_PARAMETERS)
        else:
            self.s_para = sheet_parameters

        self.optimal_area_angle=None
        self.optimal_width_angle=None
        self.optimal_length_angle=None

        self._b_pt=rg.Point3d.Origin

    @property
    def height(self):
        return self.s_para["h"]

    @height.setter
    def height(self, value):
        self.s_para["h"]=value

    @property
    def width(self):
        return self.s_para["h"]

    @width.setter
    def width(self, value):
        self.s_para["w"]=value
        
    @property
    def bottom_corner(self):
        return self._b_pt

    @bottom_corner.setter
    def bottom_corner(self, pt):
        self.move_to_position(pt-self._bottom_corner())
        self._b_pt=pt

    def update_sheet_parameters(self, s_para_dict):
        """method to update the sheet dimension dict. Should contain "w" and "h" value"""
        self.s_para=s_para_dict

    def optimize(self, opt_type="width", iterations=10):
        """method for optimizing the position on the given sheet
        input:
        opt_type   : str ("width") - whether the optimization should be for minimum
                                     "width", "length" or "area"
        iterations : int (10) - how many different angles should be checked"""

        width_angle,length_angle,area_angle,data=optimal_rec(
            self.b_pts, iterations, self.height, self.width
        )

        self.optimal_width_angle=data[width_angle]["width"]
        self.optimal_length_angle=data[length_angle]["length"]
        self.optimal_area_angle=data[area_angle]["area"]

        self.opt_a=data[opt_type]

        # positioning the whole object in the ideal location
        self.Transform(rg.Transform.Rotation(self.opt_a, centroid(self.b_pts) ) )
        self.move_to_position(-self._bottom_corner())

    def _bottom_corner(self):
        (x,y), _=bounds(self.b_pts)
        return rg.Point3d(x, y, 0.)

    def move_to_position(self, pt):
        """method to translate all the objects in this class to a given point"""
        self.Transform(rg.Transform.Translation(pt) )

    def Transform(self, t_matrix):
        """method that transforms all the objects in this class according to a give t matrix"""
        [obj.Transform(t_matrix) for obj in self.b_pts]
        [obj.Transform(t_matrix) for obj in self.f_ff]
        [obj.Transform(t_matrix) for obj in self.f_bf]
        [obj.Transform(t_matrix) for obj in self.f_if]

    def outline_crv(self):
        """method that returns the outline of the whole object"""
        return rg.PolyCurve(self.b_pts + self.b_pts[0])

    def top_face_folds(self):
        """method that returns the top face folds"""
        return self.f_ff

    def body_flap_folds(self):
        """method that returns the folds in between the main body and the flaps"""
        return self.f_bf

    def intra_flap_folds(self):
        """method that returns the folds on the flaps overlapping with other flaps"""
        return self.f_if

    def panel(self):
        """method that returns a representation of the panel"""
        rec=rg.Rectangle(rg.Plane.WorldXY, self.width, self.height).ToNurbsCurve()
        rec.Translate(self._b_pt)
        return rec