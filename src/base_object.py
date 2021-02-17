from geometries import Simple, Center, Unfolded
from geometrical_helpers import fix_pts_heights, fix_ptss_heights
from pattern_generator import *
from facade_link_info import DEFAULT_CONSTRUCTION_PARAMETERS
import Rhino.Geometry as rg

class BaseObject:
    """class used to encapsulate the different types
    all dimensions are defined in mm"""
    def __init__(self, objs=[], index=None, type_name=None, pattern_name=None, parameters=None):
        """input:
        objs         : list of objects defining this general object
        index        : uv coordinates of this object (default None)
        type_name    : name of this geometry cluster (default None)
        pattern_name : pattern type that defines the interlocking pattern of the flaps (default None)"""

        self.objs=objs

        self.name=type_name
        self.pattern=pattern_name
        self.index=index

        if parameters is None:
            global DEFAULT_CONSTRUCTION_PARAMETERS
            self.parameters=dict(DEFAULT_CONSTRUCTION_PARAMETERS)
        else:
            self.parameters=parameters

        self._call_count=0

    def get_mesh(self, placement_plane=rg.Plane.WorldXY):
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
            msh=obj.rhino_mesh(self.parameters["show_correction_val"])
            msh.Transform(t_matrix)
            msh_output.append(msh)
        
        return msh_output

    def get_2d(self, optimization_parameters={"iterations":50, "max_w":1000, "max_l": 1800, "preference":"width"}):
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

        for i, obj in enumerate(self.objs):
            b_pt=rg.Point3d(optimization_parameters["max_w"]*i, 0., 0.)
            unfolded_obj=obj.get_unfolded()

            unfolded_obj.width=optimization_parameters["max_w"]
            unfolded_obj.height=optimization_parameters["max_l"]
            unfolded_obj.optimize(
                opt_type=optimization_parameters["preference"],
                iterations=optimization_parameters["iterations"]
            )

            unfolded_obj.bottom_corner=b_pt

            unfolded_objs.append(unfolded_obj)

        return unfolded_objs

    def get_count(self):
        """method that returns how many times this object has been called to visualize"""
        return self._call_count

    def get_name(self):
        """method that returns the compound name if parameters were set"""
        string_list=[]

        if not(self.name is None):
            string_list.append(self.name)
        if not(self.pattern is None):
            string_list.append(self.pattern)
        if not(self.index is None):
            string_list.append(str(self.index))

        return ' '.join(string_list)

    def __repr__(self):
        return self.get_name()+' with {} panels in it'.format(self.get_count())

    @staticmethod
    def simple_square(pts, index = (0,0), other_parameters = None, fold_idx=None):
        """factory for simple square objects
        input:
        pts              : boundary pts
        pattern_type     : the geometry of the side flaps
        index            : the index of this object in the grid (only used for naming)
        other_parameters : other parameters defining various aspects of the geometry"""

        if other_parameters is None:
            global DEFAULT_CONSTRUCTION_PARAMETERS
            other_parameters=dict(DEFAULT_CONSTRUCTION_PARAMETERS)
        else:
            other_parameters=dict(other_parameters)
        
        if fold_idx is None:
            fold_idx=other_parameters["fold_idx"]

        fix_pts_heights(pts, other_parameters["min_pt_height"])

        pattern_type=other_parameters["pattern"]
        pattern=simple_pattern_parser(pattern_type, len(pts))
        square=Simple(pts, pattern, other_parameters, fold_idx)

        return BaseObject(
            objs=[square],
            index=index,
            type_name="simple_square",
            pattern_name=pattern_type,
            parameters=other_parameters
        )

    @staticmethod
    def simple_triangle(pts, index = (0,0), other_parameters=None):
        """factory for simple square objects
        input:
        pts              : boundary pts
        pattern_type     : the geometry of the side flaps
        index            : the index of this object in the grid (only used for naming)
        other_parameters : other parameters defining various aspects of the geometry"""
        if other_parameters is None:
            global DEFAULT_CONSTRUCTION_PARAMETERS
            other_parameters=dict(DEFAULT_CONSTRUCTION_PARAMETERS)

        fix_pts_heights(pts, other_parameters["min_pt_height"])

        pattern_type=other_parameters["pattern"]
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
    def pyramid(pts, pt, index=(0,0), other_parameters=None):
        """factory for two part pyramid object
        input:
        pts              : boundary pts
        pt               : center point
        pattern_type     : the geometry of the side flaps
        index            : the index of this object in the grid (only used for naming)
        other_parameters : other parameters defining various aspects of the geometry"""

        if other_parameters is None:
            global DEFAULT_CONSTRUCTION_PARAMETERS
            other_parameters=dict(DEFAULT_CONSTRUCTION_PARAMETERS)

        other_parameters["orient"]=False

        fix_pts_heights(pts+[pt], other_parameters["min_pt_height"])

        pattern_type=other_parameters["pattern"]
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
    def cube_group(ptss, index=(0,0), other_parameters=None):
        """factory for group of square objects
        input:
        ptss             : list of boundary pts
        pattern_type     : the geometry of the side flaps
        index            : the index of this object in the grid (only used for naming)
        other_parameters : other parameters defining various aspects of the geometry"""

        if other_parameters is None:
            global DEFAULT_CONSTRUCTION_PARAMETERS
            other_parameters=dict(DEFAULT_CONSTRUCTION_PARAMETERS)

        fix_ptss_heights(ptss, other_parameters["min_pt_height"])

        pattern_type=other_parameters["pattern"]
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

    @staticmethod
    def null_object(index=(0,0)):
        return BaseObject(
            objs=[],
            index=index,
            type_name="empty_object",
            pattern_name="null_pattern",
        )