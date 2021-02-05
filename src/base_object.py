class BaseObject:
    """class used to encapsulate the different types
    all dimensions are defined in mm"""
    def __init__(self, objs = [], index = None, type_name = None, pattern_name = None):
        """input:
        objs         : list of objects defining this general object
        index        : uv coordinates of this object (default None)
        type_name    : name of this geometry cluster (default None)
        pattern_name : pattern type that defines the interlocking pattern of the flaps (default None)"""

        self.objs = []

        self.name = type_name
        self.pattern = pattern_name
        self.index = index

        self._call_count = 0

    def get_mesh(self, placement_plane):
        """method that returns the 3d mesh representation of this object
        every time this function is called, call_count will be increased by 1
        input:
        placement_plane : plane where the mesh should be positioned"""
        self._call_count += 1
        return [obj.get_mesh(placement_plane) for obj in self.objs]

    def get_2d(self, optimization_parameters = {"iterations":50, "max_w":1000, "max_l": 1800, "preference":"width"}):
        """method that returns the 2d unfoulded geometry of this objects
        input:
        optimization_parameters : dict used to position the geometry as good as possible for production
                                  custon dict should contain:
                                    max_l : float (default 1800),
                                    max_w : float (default 1000),
                                    iterations : int (default 50),
                                    preference : ["area", "width", "length"] (default: "width")"""
        
        return [obj.get_2d(optimization_parameters, i) for i, obj in enumerate(self.objs)] #get_2d should be able to take index so it can be spaced correctly

    def get_count(self):
        """method that returns how many times this object has been called to visualize"""
        return self._call_count

    def get_name(self):
        """method that returns the compound name if parameters were set"""
        string = ''

        if not(self.name is None):
            string += self.name
        if not(self.pattern is None):
            string += self.pattern
        if not(self.index is None):
            string += str(self.index)

        return string

    @staticmethod
    def simple_square(pts, pattern_type = "flat", index = (1,1) ):
        return BaseObject(square)