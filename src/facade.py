from base_object import BaseObject
from Rhino.Geometry import Plane, Point3d, Vector3d

class FacademakerFacade:
    """Facademaker Container Class"""
    X_VEC=Vector3d(1.0,0,0)
    Z_VEC=Vector3d(0,0,1.0)

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

        self.objects_per_tile=1
        self.selection_pattern=[[1]]
        self.layer_shift=0

    def update_objects(self, object_idx, object_lists):
        """method that adds or updates the base objects groups of this facade"""
        self.base_objs[object_idx]=object_lists

    @property
    def base_count(self):
        return self.dimension[0]*self.dimension[1]

    def _o_p_t_rnd(self, value):
        """internal method that return the index of the reference plane to be considered
        for a given object"""
        return int((value-value%self.objects_per_tile)/self.objects_per_tile)

    def _sel_obj_idx(self, z_i, x_i):
        """internal method that returns the obj value that should be used for a given cell"""
        z_idx=z_i%len(self.selection_pattern)
        x_idx=x_i%len(self.selection_pattern[0])

        selection_idx=self.selection_pattern[z_idx][x_idx]
        if selection_idx!=1:
            print("selecting non standard selection_idx: {}".format(selection_idx))
        return selection_idx

    def populate(self):
        """method that returns a mesh population of the whole facade with custom objects"""
        mshs=[]

        for i in range(self.z_cnt):
            start_idx=i*self.objects_per_tile*self.layer_shift
            for j in range(self.x_cnt*self.objects_per_tile):
                b_pln=Plane(
                    Point3d(self._o_p_t_rnd(j)*self.x_dim, 0, i*self.z_dim),
                    FacademakerFacade.X_VEC,
                    FacademakerFacade.Z_VEC
                )

                b_obj_idx=self._sel_obj_idx(i,j)
                z_idx_obj=i%len(self.base_objs[b_obj_idx])
                x_idx_obj=(start_idx+j)%len(self.base_objs[b_obj_idx][0])
                obj=self.base_objs[b_obj_idx][z_idx_obj][x_idx_obj]

                mshs.extend(obj.get_mesh(b_pln))

        return mshs

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

    def set_selection_pattern(self, selection_pattern = [[1]], layer_shift=0):
        """set the pattern with which should be used to fill the facade
        input:
        selection_pattern   : list of list of key entries that will be used when populating
        layer_shift         : when populating, at which index one should start in the respective row"""
        self.selection_pattern=selection_pattern
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
        self.objects_per_tile=2

    def set_quad_block(self, ptss, other_parameters=None, obj_idx=1):
        """assign group of 4 point objects"""
        self.base_objs[obj_idx]=[[BaseObject.cube_group(
            ptss=ptss,
            index=(0,0),
            other_parameters=other_parameters
        )]]

    def set_multi_squares(self, ptsss, other_parameters=None, obj_idx=1, fold_idxs=[[0]]):
        """assign a n.m list of 4 point objects"""
        self.base_objs[obj_idx]=[]
        for i, ptss in enumerate(ptsss):
            base_obj_row=[]
            for j, pts in enumerate(ptss):
                fold_idx=fold_idxs[i%len(fold_idxs)][j%len(fold_idxs[0])]
                base_obj_row.append(BaseObject.simple_square(
                    pts=pts,
                    index=(i,j),
                    other_parameters=other_parameters,
                    fold_idx=fold_idx
                ))
            self.base_objs[obj_idx].append(base_obj_row)
        self.set_dimension((i+1,j+1))

    def set_multi_pyramids(self, ptsss, c_ptss, other_parameters=None, obj_idx=1):
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

    def set_multi_triangles(self, ptsss, other_parameters=None, obj_idx=1):
        """assign a n.m list of 4 point objects"""
        self.base_objs[obj_idx]=[]
        for i, ptss in enumerate(ptsss):
            base_obj_row=[]
            for j, pts in enumerate(ptss):
                base_obj_row.append(BaseObject.simple_triangle(
                    pts=pts,
                    index=(i,j),
                    other_parameters=other_parameters
                ))
            self.base_objs[obj_idx].append(base_obj_row)
        self.set_dimension((i+1,j+1))

    def set_multi_quad_blocks(self, ptssss, other_parameters=None, obj_idx=1):
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
