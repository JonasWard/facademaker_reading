class FacademakerFacade:
    """Facademaker Container Class"""
    def __init__(self, length, height):
        """Initializing the facade with a give length and height"""
        self.l = length
        self.h = height

        self.dimension = (1,1)
        self.base_objs = {
            0: None,
            1: []
        }

        self.filling_pattern = [1]

    def populate(self, base_objs, obj_type = 1):
        """populate the facade with custom objects
        input
            base_objs : single, list or nested list of objects
            obj_type  : obj index (in case multiple objects are defined) - default 1
        """
        if isinstance(base_objs, list):
            if isinstance(base_objs[0], list):
                self.base_objs[obj_type] = base_objs
            else:
                self.base_objs[obj_type] = [base_objs]
        else:
            self.base_objs[obj_type] = [[base_objs]]
        
        if obj_type == 1:
            self.dimension = (len(base_objs[0]), len(base_objs))
            print("set a new dimension of the base facade building block: {} x {}".format(
                self.dimension[0],
                self.dimension[1]
            ) )

    def set_pattern(self, culling_pattern = [1]):
        """set the pattern with which the facade should be filled"""
        self.filling_pattern = culling_pattern
