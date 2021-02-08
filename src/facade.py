from base_object import BaseObject

class FacademakerFacade:
    """Facademaker Container Class"""
    def __init__(self, x_count, z_count, x_spacing, z_spacing):
        """Initializing the facade with a give length and height"""
        self.x_cnt=x_count
        self.z_cnt=z_count

        self.x_dim=x_spacing
        self.z_dim=z_spacing

        self.dimension = [1,1]
        self.base_objs = {
            0: [[BaseObject.null_object()]],
            1: [[]]
        }

        self.culling_pattern=[1]
        self.layer_shift=0

    def update_objects(self, object_idx, object_lists):
        """method that adds or updates the base objects groups of this facade"""
        self.base_objs[object_idx]=object_lists

    @property
    def base_count(self):
        return self.dimension[0]*self.dimension[1]

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

    def set_dimension(self, dim_tuple):
        m,n=dim_tuple
        print("new dimension {} x {} has been set".format(m,n))
        self.dimension=dim_tuple

    @property
    def all_base_objects(self):
        all_b_objs=[]
        for value in self.base_objs.values():
            for row in value:
                for obj in row:
                    all_b_objs.append(obj)
        return all_b_objs

    def set_culling_pattern(self, culling_pattern = [1], layer_shift=0):
        """set the pattern with which the facade should be filled"""
        self.culling_pattern=culling_pattern
        self.layer_shift=layer_shift

    def set_square(self, pts, other_parameters=None, obj_idx=1):
        """assign 4 point objects"""
        self.base_objs[obj_idx]=[[BaseObject.simple_square(
            pts=pts, 
            index=(0,0), 
            other_parameters=other_parameters
        )]]

    def set_pyramid(self, pts, c_pt, other_parameters=None, obj_idx=1):
        """assign 4 point pyramid objects"""
        self.base_objs[obj_idx]=[[BaseObject.pyramid(
            pts=pts, 
            pt=c_pt, 
            index=(0,0), 
            other_parameters=other_parameters
        )]]

    def set_triangle_pair(self, ptss, other_parameters=None, obj_idx=1):
        """assign 2 triangle objects"""
        base_obj_row=[]
        for j, pts in enumerate(ptss):
            base_obj_row.append(BaseObject.simple_triangle(
                pts=pts,
                index=(0,j), 
                other_parameters=other_parameters
            ))
        self.base_objs[obj_idx]=[base_obj_row]
        self.set_dimension((1,j+1))

    def set_quad_block(self, ptss, other_parameters=None, obj_idx=1):
        """assign group of 4 point objects"""
        self.base_objs[obj_idx]=[[BaseObject.cube_group(
            ptss=ptss,
            index=(0,0),
            other_parameters=other_parameters
        )]]

    def set_multi_square(self, ptsss, other_parameters=None, obj_idx=1):
        """assign a n.m list of 4 point objects"""
        self.base_objs[obj_idx]=[]
        for i, ptss in enumerate(ptsss):
            base_obj_row=[]
            for j, pts in enumerate(ptss):
                base_obj_row.append(BaseObject.simple_square(
                    pts=pts,
                    index=(i,j),
                    other_parameters=other_parameters
                ))
            self.base_objs[obj_idx].append(base_obj_row)
        self.set_dimension((i+1,j+1))

    def set_multi_pyramid(self, ptsss, c_ptss, other_parameters=None, obj_idx=1):
        """assign a n.m list of 4 point pyramid objects"""
        self.base_objs[obj_idx]=[]
        for i, ptss in enumerate(ptsss):
            base_obj_row=[]
            for j, pts in enumerate(ptss):
                base_obj_row.append(BaseObject.pyramid(
                    pts=pts,
                    pt=c_ptss[i][j],
                    index=(i,j),
                    other_parameters=other_parameters
                ))
            self.base_objs[obj_idx].append(base_obj_row)
        self.set_dimension((i+1,j+1))

    def set_multi_quad_block(self, ptssss, other_parameters=None, obj_idx=1):
        """assign a n.m list of quad_block objects"""
        self.base_objs[obj_idx]=[]
        for i, ptsss in enumerate(ptssss):
            base_obj_row=[]
            for j, ptss in enumerate(ptsss):
                base_obj_row.append(BaseObject.cube_group(
                    ptss=ptss,
                    index=(i,j),
                    other_parameters=other_parameters
                ))
            self.base_objs[obj_idx].append(base_obj_row)
        self.set_dimension((i+1,j+1))
