from geometries import Simple, Center, Unfolded
from pattern_generator import *
import Rhino.Geometry as rg

class BaseObject:
    DEFAULT_PARAMETERS = {
        "flap_h_max" : 30.,
        "correction_val" : .7,
        "flap_h" : 20.0,
        "flap_w" : 40.0,
        "mesh_correction_val" : False,
        "show_correction_val" : True
    }

    """class used to encapsulate the different types
    all dimensions are defined in mm"""
    def __init__(self, objs=[], index=None, type_name=None, pattern_name=None, parameters=None):
        """input:
        objs         : list of objects defining this general object
        index        : uv coordinates of this object (default None)
        type_name    : name of this geometry cluster (default None)
        pattern_name : pattern type that defines the interlocking pattern of the flaps (default None)"""

        self.objs=[]

        self.name=type_name
        self.pattern=pattern_name
        self.index=index

        if parameters is None:
            self.parameters=dict(BaseObject.DEFAULT_PARAMETERS)
        else:
            self.parameters=parameters

        self._call_count=0

    def get_mesh(self, placement_plane):
        """method that returns the 3d mesh representation of this object
        every time this function is called, call_count will be increased by 1
        input :
        placement_plane : plane where the mesh should be positioned
        return :
        msh_output      : list of meshes"""
        self._call_count += 1

        t_matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, placement_plane)
        msh_output = []

        for obj in self.objs:
            msh = rg.Mesh(obj.get_mesh(self.parameters["show_correction_val"]) )
            msh.Transform(t_matrix)
            msh_output.append(msh)
        
        return msh_output

    def get_2d(self, optimization_parameters = {"iterations":50, "max_w":1000, "max_l": 1800, "preference":"width"}):
        """method that returns the 2d unfoulded geometry of this objects
        input:
        optimization_parameters : dict used to position the geometry as good as possible for production
                                  custon dict should contain:
                                    max_l : float (default 1800),
                                    max_w : float (default 1000),
                                    iterations : int (default 50),
                                    preference : ["area", "width", "length"] (default: "width")
        return:
        unfolded_objs           : list of unfolded objects"""
        
        unfolded_objs = []
        for obj, i in enumerate(self.objs):
            b_pt=rg.Point3d(optimization_parameters["max_w"]*i, 0., 0.)
            unfolded_obj=obj.get_unfolded()
            unfolded_obj.bottom_corner=b_pt

            unfolded_objs.append(unfolded_obj)

        return unfolded_objs

    def get_count(self):
        """method that returns how many times this object has been called to visualize"""
        return self._call_count

    def get_name(self):
        """method that returns the compound name if parameters were set"""
        string = ''

        if not(self.name is None):
            string+=self.name
        if not(self.pattern is None):
            string+=self.pattern
        if not(self.index is None):
            string+=str(self.index)

        return string

    @staticmethod
    def simple_square(pts, pattern_type = "flat", index = (0,0), other_parameters = None):
        """factory for simple square objects
        input:
        pts              : boundary pts
        pattern_type     : the geometry of the side flaps
        index            : the index of this object in the grid (only used for naming)
        other_parameters : other parameters defining various aspects of the geometry"""
        if other_parameters is None:
            other_parameters=BaseObject.DEFAULT_PARAMETERS

        pattern=simple_pattern_parser(pattern_type, len(pts))
        square=Simple(pts, pattern, other_parameters)

        return BaseObject(
            objs=[square],
            index=index,
            type_name="simple_square",
            pattern_name=pattern_type,
            parameters=other_parameters
        )

    @staticmethod
    def simple_triangle(pts, pattern_type="flat", index = (0,0), other_parameters=None):
        """factory for simple square objects
        input:
        pts              : boundary pts
        pattern_type     : the geometry of the side flaps
        index            : the index of this object in the grid (only used for naming)
        other_parameters : other parameters defining various aspects of the geometry"""
        if other_parameters is None:
            other_parameters = dict(BaseObject.DEFAULT_PARAMETERS)

        pattern = simple_pattern_parser(pattern_type, len(pts))
        triangle = Simple(pts, pattern, other_parameters)

        return BaseObject(
            objs=[triangle],
            index=index,
            type_name="simple_triangle",
            pattern_name=pattern_type,
            parameters=other_parameters
        )

    @staticmethod
    def pyramid(pts, pt, pattern_type="flat", index=(0,0), other_parameters=None):
        """factory for two part pyramid object
        input:
        pts              : boundary pts
        pt               : center point
        pattern_type     : the geometry of the side flaps
        index            : the index of this object in the grid (only used for naming)
        other_parameters : other parameters defining various aspects of the geometry"""
        if other_parameters is None:
            other_parameters=BaseObject.DEFAULT_PARAMETERS

        pentagon_pattern, triangle_pattern=pyramid_pattern_parser(pattern_type, len(pts) )
        top_pentagon=Center(pts, pt, pentagon_pattern, other_parameters)
        triangle=Simple([pts[0],pt,pts[-1]], triangle_pattern, other_parameters)

        return BaseObject(
            objs=[top_pentagon, triangle],
            index=index,
            type_name="diamond",
            pattern_name=pattern_type,
            parameters=other_parameters
        )

    @staticmethod
    def cube_group(ptss, pattern_type="flat", index=(0,0), other_parameters=None):
        """factory for group of square objects
        input:
        ptss             : list of boundary pts
        pattern_type     : the geometry of the side flaps
        index            : the index of this object in the grid (only used for naming)
        other_parameters : other parameters defining various aspects of the geometry"""
        if other_parameters is None:
            other_parameters=BaseObject.DEFAULT_PARAMETERS

        cube_group_patterns=cube_group_pattern_parser(pattern_type, (len(ptss[0]), len(ptss)))

        objs=[]
        for i, pts in enumerate(ptss):
            objs.append(Simple(pts, cube_group_patterns[i], other_parameters) )

        return BaseObject(
            objs=objs,
            index=index,
            type_name="cube_group",
            pattern_name=pattern_type,
            parameters=other_parameters
        )