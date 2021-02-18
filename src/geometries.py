import Rhino.Geometry as rg
import math
from unfolded import Unfolded
from pattern_generator import simple_pattern_parser
from facade_link_info import DEFAULT_CONSTRUCTION_PARAMETERS
from panel_sides import *

class Base():
    """Main geometric solution class allowing for a given set of boundary points
    to generate a mesh, unfolding it, adding flaps and calculating the sides, and
    two different methods of incalculating tolerances. All the function in this 
    class are called in it's offspring classes."""

    COPLANAR_TOLERANCE=.5

    def projected_pts(self, offset=False):
        """projects the input points onto the bottom surface
        stores those projected point into the class"""
        pts=self.ori_pts if (not(offset) and self.has_offset) else self.pts
        return [rg.Point3d(pt.X, pt.Y, 0.0) for pt in pts]

    def start_run(self):
        """initialization method"""
        global DEFAULT_CONSTRUCTION_PARAMETERS

        self.pattern = simple_pattern_parser(cnt=len(self.pts))
        self.s_p_p = dict(DEFAULT_CONSTRUCTION_PARAMETERS)
        self.has_graph=False
        self.has_offset=False
        self.has_holes=False
        self.ori_pts=self.pts[:]
        self._f_list=[]
        self._is_unfolded=False
        self._has_sides=False
        self.unfolded=None

    @property
    def f_list(self):
        if any(self._f_list):
            return self._f_list
        else:
            print("""face list has not been populated yet, either construct_graph hasn't
            been initialized yet or it failed to construct.""")

    @property
    def count(self):
        """method that returns the amount of corner points in this object"""
        return len(self.pts)

    @property
    def cor_val(self):
        return self.s_p_p["correction_val"]

    @property
    def with_cor_val_3d(self):
        return self.s_p_p["show_correction_val"]

    def _pt_distance_mapping(self, pts, new_pt_list):
        new_pts=[]
        for pt in pts:
            distances=[pt.DistanceTo(n_pt) for n_pt in new_pt_list]
            distances, new_pt_list=zip(*sorted(zip(distances, new_pt_list) ) )

            new_pts.append(new_pt_list[0])

        return new_pts

    def polyline_correction(self):
        """offsetting the polyline composed of the projected boundary curve
        to adjust the position of the vertexes with to compensate for folding
        tolerance - more representative result"""

        print("calling polyline correction")

        pts=self.projected_pts(False)
        n_pl=rg.PolylineCurve(pts+[pts[0]]).Offset(
            rg.Plane.WorldXY, -self.cor_val, .001, rg.CurveOffsetCornerStyle.Sharp
        )[0]

        new_pt_list=list(n_pl.ToPolyline() )[:-1]

        new_pts=self._pt_distance_mapping(pts, new_pt_list)

        for i, pt in enumerate(self.pts):
            new_pts[i].Z=pt.Z-abs(self.cor_val)

        self.has_offset=True
        self.pts=new_pts

    def mesh_correction(self):
        """offsetting the mesh structure to adjust the position of the vertexes 
        with to compensate for folding tolerance - angle deformation susceptible"""

        mesh_obj=self.rhino_mesh()
        offsetted=mesh_obj.Offset(self.cor_val)

        new_pt_list=[rg.Point3d(v.X,v.Y,v.Z) for v in list(offsetted.Vertices)]

        new_pts=self._pt_distance_mapping(self.pts, new_pt_list)

        self.has_offset=True
        self.pts=new_pts

    def orient_pts(self, pts, start_idx=0):
        """method that sorts all the points counter-clockwise around the
        polygons centroid"""

        c_pt=centroid(pts)
        pt_copy=[pt-c_pt for pt in pts]

        angles=[math.atan2(pt.Y, pt.X) for pt in pt_copy]
        angles, pts=zip(*sorted(zip(angles, pts) ) )
        
        pts=list(pts)
        return pts[start_idx:]+pts[:start_idx]

    def is_coplanar(self):
        """method that check whether the original points are coplanar"""
        return rg.Point3d.ArePointsCoplanar(self.pts, Base.COPLANAR_TOLERANCE)

    def construct_graph(self):
        """method that constructs the connection graph of all the faces"""

        v_list=[i for i in range(self.count) ]
        v_list.pop(0)
        f_list=[]
        # print(v_list)
        for i in range(self.count - 2):
            v_a=v_list.pop(0)
            f_list.append((0, v_a, v_list[0]))

        self.has_graph=True
        self._f_list=f_list

    def rhino_brep(self):
        """method that returns a rhino brep representation of the object
        input:
        offset      : bool (True)  - whether to use the corrected pts for construction
        brep_offset : bool (False) - whether you want to offset the brep representation
        brep_offset : float (1.0)  - how much the brep offset value should be
        output:
        surface     : rg.Brep"""
        pts=self.ori_pts if (not(self.with_cor_val_3d) and self.has_offset) else self.pts
        
        vertices=pts+self.projected_pts(self.cor_val)
        f_list=self.f_list[:]

        for i in range(self.count ):
            f_list.append([
                (i+1)%self.count,
                i,
                self.count+i,
                self.count+(i+1)%self.count
            ])

        for f in self.f_list:
            f_list.append([
                self.count+f[2],
                self.count+f[1],
                self.count+f[0]
            ])

        # pt_list=[[vertices[f[0]], vertices[f[1]], vertices[f[2]]] for f in f_list]
        
        surfaces=[]
        for f in f_list:
            if len(f)==3:
                surfaces.append(
                    rg.Brep().CreateFromCornerPoints(
                        vertices[f[0]], vertices[f[1]], vertices[f[2]], .001
                ) )

            elif len(f) == 4:
                surfaces.append(
                    rg.Brep().CreateFromCornerPoints(
                        vertices[f[0] ], vertices[f[1] ], vertices[f[2] ], vertices[f[3] ], .001
                ) )

        surface=rg.Brep.JoinBreps(surfaces, .001)[0]

        # if brep_offset:
        #     surface_array=rg.Brep.CreateOffsetBrep(
        #         brep=surface,
        #         distance=self.cor_val,
        #         solid=False,
        #         extend=False,
        #         tolerance=.01,
        #     )

        #     if any(surface_array[0]):
        #         surface=surface_array[0][0]
        #         print("offset success")
        #     else:
        #         print("offset failed")

        return surface

    def rhino_mesh(self):
        """method that returns a rhino brep representation of the object
        output:
        mesh        : rg.Mesh"""
        mesh=rg.Mesh()

        pts=self.ori_pts if (not(self.with_cor_val_3d) and self.has_offset) else self.pts

        # top faces
        for pt in pts:
            mesh.Vertices.Add(pt.X, pt.Y, pt.Z)
        for f in self.f_list:
            mesh.Faces.AddFace(f[0], f[1], f[2])

        # bottom vertices
        for pt in self.projected_pts(pts):
            mesh.Vertices.Add(pt.X, pt.Y, pt.Z)
        # side faces
        for i in range(self.count ):
            mesh.Faces.AddFace(
                (i+1)%self.count,
                i,
                self.count + i,
                self.count + (i+1)%self.count
            )
        # bottom face
        for f in self.f_list:
            mesh.Faces.AddFace(
                self.count + f[2],
                self.count + f[1],
                self.count + f[0]
            )

        return mesh

    def edge_length(self, idx_0, idx_1):
        return self.pts[idx_0].DistanceTo(self.pts[idx_1])

    def _unfold_face(self, idx_0, idx_1, idx_2):
        self.flat_pts={
            idx_0:rg.Point3d(0,0,0),
            idx_1:rg.Point3d(self.edge_length(idx_0, idx_1), 0.0, 0.0)
        }

        self._unfold_vertex(idx_2, idx_0, idx_1)

    def _unfold_vertex(self, idx, idx_ref_0, idx_ref_1):
        # print(idx)
        # print(self.flat_pts)
        self.flat_pts[idx]=triangulate(
            self.flat_pts[idx_ref_0],
            self.flat_pts[idx_ref_1],
            self.edge_length(idx, idx_ref_0),
            self.edge_length(idx, idx_ref_1)
        )

    def unfolding(self):
        """method that unfolds the whole object
        return:
        self.flat_pts : list of points representing the outline of the geometry"""

        folded_list=dict((i, False) for i in range(self.count ) )

        loc_f_graph=self.f_list[:]
        first_face=loc_f_graph.pop(0)
        self._unfold_face(first_face[0], first_face[1], first_face[2])

        for idx in first_face:
            folded_list[idx]=True

        while any(loc_f_graph):
            for f_idx, f in enumerate(loc_f_graph):
                fixed_vertex_count=0
                for idx, v in enumerate(f):
                    if folded_list[v]:
                        fixed_vertex_count += 1
                    else:
                        to_resolve_idx=idx

                if fixed_vertex_count == 2:
                    break

            current_face=loc_f_graph.pop(f_idx)

            self._unfold_vertex(
                current_face[to_resolve_idx],
                current_face[ (to_resolve_idx+1)%3 ],
                current_face[ (to_resolve_idx-1)%3 ]
            )

            folded_list[current_face[to_resolve_idx] ] = True

        self._is_unfolded=True
        return self.flat_pts

    @property
    def h_max(self):
        return self.s_p_p["flap_h_max"]

    @property
    def flap_h(self):
        return self.s_p_p["flap_h"]

    @property
    def flap_w(self):
        return self.s_p_p["flap_w"]

    def fold_lns(self):
        """method that returns all the main fold lines of the flattened top surface"""
        if not(self._is_unfolded):
            self.unfolding()
        
        folds=[]
        flattened_graph=[]

        for f in self.f_list:
            flattened_graph.extend(f)

        unique=list(set(flattened_graph))
        unique.remove(0)

        u_dict=dict((idx, 0) for idx in unique)

        f_graph=list(filter(lambda a: a != 0, flattened_graph))
        for val in f_graph:
            u_dict[val]+=1

        for key, val in u_dict.items():
            if val == 2:
                folds.append(rg.Line(self.flat_pts[key], self.flat_pts[0]))

        return folds

    def add_simple_sides(self):
        """depreciated method for creating flat sides"""
        
        if not(self._is_unfolded):
            self.unfolding()
        
        outline_pts=[]
        folds=[]
        for i in range(self.count ):
            idx_0=i
            idx_1=(i + 1) % self.count

            pt_0=self.pts[idx_0]
            pt_1=self.pts[idx_1]

            pt_0_new=self.flat_pts[idx_0]
            pt_1_new=self.flat_pts[idx_1]

            outline_pts.append(pt_0_new)
            pts, loc_folds = PanelSideSegment(pt_0, pt_1).simple_side(pt_0_new, pt_1_new)
            outline_pts.extend(pts)
            folds.extend(loc_folds)

        return outline_pts+[pt_1_new], folds, []

    def add_sides(self):
        """method that add sides to the unfolded object as defined in the pattern map"""

        if not(self._is_unfolded):
            self.unfolding()

        outline_pts=[]
        folds_a=[] # main folds between flap and main body
        folds_b=[] # folds on the flaps to be able to interlock them

        for i in range(self.count):

            loc_pattern=self.pattern[i]

            idx_0=i
            idx_1=(i + 1) % self.count

            pt_0=self.pts[idx_0]
            pt_1=self.pts[idx_1]

            pt_0_new=self.flat_pts[idx_0]
            pt_1_new=self.flat_pts[idx_1]

            outline_pts.append(pt_0_new)
            if isinstance(loc_pattern, tuple) or isinstance(loc_pattern, list):
                pts, loc_folds_a, loc_folds_b = PanelSideSegment(pt_0, pt_1).complex_side(
                    pt_0_new,
                    pt_1_new,
                    self.h_max,
                    loc_pattern
                )
            elif isinstance(loc_pattern, str):
                if loc_pattern=="flap":
                    pts, loc_folds_a = PanelSideSegment(pt_0_new, pt_1_new).simple_flap(self.flap_h, self.flap_w, False)
                    loc_folds_b = []
                else:
                    print("undifined simple type: {}".format(loc_pattern))
                    pts, loc_folds_a, loc_folds_b = [], [], []
            else:
                print("undifined complex pattern type: {}".format(loc_pattern))
                pts, loc_folds_a, loc_folds_b = [], [], []

            outline_pts.extend(pts)
            folds_a.extend(loc_folds_a)
            folds_b.extend(loc_folds_b)

        if not(self.is_coplanar()):
            top_face_folds=self.fold_lns()
        else:
            top_face_folds=[]

        self.unfolded=Unfolded(
            boundary=outline_pts,
            top_face_folds=top_face_folds,
            body_flap_folds=folds_a, 
            intra_flap_folds=folds_b
        )

        self._has_sides=True

    def get_unfolded(self):
        """method that returns the unfolded version of the object"""

        if not(self._has_sides):
            self.add_sides()
        
        return self.unfolded

class Simple(Base):
    def __init__(self, pts, pattern = None, production_parameters=None, fold_idx=None):
        if len(pts) < 3:
            print("You need to input more than 3 boundary points")
            return None
        self.pts=pts

        self.start_run()
        if not(production_parameters is None):
            print("Simple geometry got custom production_parameters")
            self.s_p_p=production_parameters

        if fold_idx is None:
            fold_idx=self.s_p_p["fold_idx"]

        if production_parameters["orient"]:
            print("Simple geometry: points have been oriented")
            self.pts=self.orient_pts(pts, start_idx=fold_idx%len(pts))

        if not(pattern is None):
            self.pattern = pattern
        else:
            print("no pattern was given, a default one has been assigned")

        self.construct_graph()

        print(str(self)+" has cor_val: {} and will {}be shown with it".format(
            self.cor_val, ["not ", ""][int(self.with_cor_val_3d)]))

        if self.with_cor_val_3d:
            self.polyline_correction()

class Center(Base):
    def __init__(self, boundary, center, pattern = None, production_parameters=None):
        if len(boundary) < 3:
            print("You need to input more than 3 boundary points")
            return None
        self.pts=boundary

        self.start_run()
        if not(production_parameters is None):
            print("Center geometry got custom production_parameters")
            self.s_p_p = production_parameters

        if production_parameters["orient"]:
            print("Center geometry: points have been oriented")
            self.pts=self.orient_pts(self.pts, 0)
        self.pts=[center]+self.pts

        if not(pattern is None):
            self.pattern = pattern
        else:
            print("no pattern was given, a default one has been assigned")

        self.construct_graph()

        print(str(self)+" has cor_val: {} and will {}be shown with it".format(
            self.cor_val, ["not ", ""][int(self.with_cor_val_3d)]))

        if self.with_cor_val_3d:
            self.polyline_correction()
