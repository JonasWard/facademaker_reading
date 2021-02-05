import Rhino.Geometry as rg
import math
from geometrical_helpers import *
from panel_sides import *

class Base():
    """Main geometric solution class allowing for a given set of boundary points
    to generate a mesh, unfolding it, adding flaps and calculating the sides, and
    two different methods of incalculating tolerances. All the function in this 
    class are called in it's offspring classes."""

    def projected_pts(self, offset=False):
        """projects the input points onto the bottom surface
        stores those projected point into the class"""
        pts=self.ori_pts if (not(offset) and self.has_offset) else self.pts
        return [rg.Point3d(pt.X, pt.Y, 0.0) for pt in pts]

    def start_run(self):
        """initialization method"""
        self.has_graph=False
        self.has_offset=False
        self.has_holes=False
        self.ori_pts=[]
        self._f_list=[]

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

    def _pt_distance_mapping(self, pts, new_pt_list):
        new_pts=[]
        for pt in pts:
            distances=[pt.DistanceTo(n_pt) for n_pt in new_pt_list]
            distances, new_pt_list=zip(*sorted(zip(distances, new_pt_list) ) )

            new_pts.append(new_pt_list[0])

        return new_pts

    def polyline_correction(self, value):
        pts=self.projected_pts(False)
        n_pl=rg.PolylineCurve(pts+[pts[0]]).Offset(
            rg.Plane.WorldXY, -value, .001, rg.CurveOffsetCornerStyle.Sharp
        )[0]

        new_pt_list=list(n_pl.ToPolyline() )[:-1]

        new_pts=self._pt_distance_mapping(pts, new_pt_list)

        for i, pt in enumerate(self.pts):
            new_pts[i].Z=pt.Z-abs(value)

        self.ori_pts=self.pts[:]
        self.has_offset=True
        self.pts=new_pts

    def mesh_correction(self, value):
        mesh_obj=self.rhino_mesh()
        offsetted=mesh_obj.Offset(value)

        new_pt_list=[rg.Point3d(v.X,v.Y,v.Z) for v in list(offsetted.Vertices)]

        new_pts=self._pt_distance_mapping(self.pts, new_pt_list)

        self.ori_pts=self.pts[:]
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
        self._f_list = f_list

    def rhino_brep(self, offset=True, brep_offset=False, brep_offset_val=1.0):
        pts=self.ori_pts if (not(offset) and self.has_offset) else self.pts
        
        vertices=pts+self.projected_pts(offset)
        f_list=self.f_list[:]

        for i in range(self.count ):
            f_list.append([
                (i+1)%self.count,
                i,
                self.count + i,
                self.count + (i+1)%self.count
            ])

        for f in self.f_list:
            f_list.append([
                self.count + f[2],
                self.count + f[1],
                self.count + f[0]
            ])

        pt_list=[[vertices[f[0]], vertices[f[1]], vertices[f[2]]] for f in f_list]
        
        surfaces=[]
        for f in f_list:
            if len(f) == 3:
                surfaces.append(
                    rg.Brep().CreateFromCornerPoints(
                        vertices[f[0] ], vertices[f[1] ], vertices[f[2] ], .001
                ) )

            elif len(f) == 4:
                surfaces.append(
                    rg.Brep().CreateFromCornerPoints(
                        vertices[f[0] ], vertices[f[1] ], vertices[f[2] ], vertices[f[3] ], .001
                ) )

        surface=rg.Brep.JoinBreps(surfaces, .001)[0]

        print(surface)

        if brep_offset:
            surface_array=rg.Brep.CreateOffsetBrep(
                brep=surface,
                distance=brep_offset_val,
                solid=False,
                extend=False,
                tolerance=.01,
            )

            print(surface_array)
            if any(surface_array[0]):
                surface=surface_array[0][0]
                print("offset success")
            else:
                print("offset failed")

        return surface

    def rhino_mesh(self, offset=True):
        mesh=rg.Mesh()

        pts=self.ori_pts if (not(offset) and self.has_offset) else self.pts

        # top faces
        for pt in pts:
            mesh.Vertices.Add(pt.X, pt.Y, pt.Z)
        for f in self.f_list:
            mesh.Faces.AddFace(f[0], f[1], f[2])

        # bottom vertices
        for pt in self.projected_pts(offset):
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

                # print("fixed vertex count: ", fixed_vertex_count)
                if fixed_vertex_count == 2:
                    # print("I should continue now")
                    break

            current_face=loc_f_graph.pop(f_idx)

            # print("faces: ", current_face)
            # print("main idx: ", to_resolve_idx)

            self._unfold_vertex(
                current_face[to_resolve_idx],
                current_face[ (to_resolve_idx+1)%3 ],
                current_face[ (to_resolve_idx-1)%3 ]
            )

            folded_list[current_face[to_resolve_idx] ] = True

        return self.flat_pts

    def fold_lns(self):
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

    def pattern_maker(self, pattern):
        pattern=[(2,2)] if pattern is None else pattern

        if isinstance(self, Simple):
            pattern=[pattern[i%len(pattern)] for i in range(self.count ) ]
        elif isinstance(self, Center) or isinstance(self, ClosedPyramid) and not(pattern[0]==3 and pattern[-1]==3):
            pattern=[3]+[pattern[i%len(pattern)] for i in range(self.count-2)]+[3]

        return pattern

    def add_simple_sides(self):
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

    def add_complex_sides(self, h_max=5.0, flap_h=20.0, flap_w=40.0, pattern=None):
        pattern=self.pattern_maker(pattern)
        # print(flap_h, flap_w)

        outline_pts=[]
        folds_a=[]
        folds_b=[]
        for i in range(self.count ):

            pattern_type=pattern[i]

            idx_0=i
            idx_1=(i + 1) % self.count

            pt_0=self.pts[idx_0]
            pt_1=self.pts[idx_1]

            pt_0_new=self.flat_pts[idx_0]
            pt_1_new=self.flat_pts[idx_1]

            outline_pts.append(pt_0_new)
            if isinstance(pattern_type, tuple) or isinstance(pattern_type, list):
                pts, loc_folds_a, loc_folds_b = PanelSideSegment(pt_0, pt_1).complex_side(
                    pt_0_new,
                    pt_1_new,
                    h_max,
                    pattern_type
                )
            elif isinstance(pattern_type, int):
                if pattern_type==3:
                    pts, loc_folds_a = PanelSideSegment(pt_0_new, pt_1_new).simple_flap(flap_h, flap_w, False)
                    loc_folds_b = []
                else:
                    print("undifined pattern int: {}".format(pattern_type))
                    pts, loc_folds_a, loc_folds_b = [], [], []
            else:
                print("undifined pattern type: {}".format(pattern_type))
                pts, loc_folds_a, loc_folds_b = [], [], []

            outline_pts.extend(pts)
            folds_a.extend(loc_folds_a)
            folds_b.extend(loc_folds_b)

        return outline_pts+[pt_1_new], folds_a, folds_b

    def unfold_object(self, with_inner_folds=True):
        pass
        # return Unfolded(
        #     source=self,
        #     boundary=self.pts,
        #     folds_flaps_a=
        #     folds_flaps_b=
        #     holes=[]
        # )

class Simple(Base):
    def __init__(self, pts, idx=0, orient=True):
        self.start_run()
        if len(pts) < 3:
            print("You need to input more than 3 points")
            return None
        self.pts=pts
        if orient:
            self.pts=self.orient_pts(pts, start_idx=idx%len(pts))

        self.construct_graph()

class Center(Base):
    def __init__(self, boundary, center, orient=True):
        self.start_run()
        self.pts=boundary
        if orient:
            self.pts=self.orient_pts(self.pts, 0)
        self.pts=[center]+self.pts

        self.construct_graph()

class ClosedPyramid(Base):
    def __init__(self, boundary, center, orient=True):
        self.start_run()
        if orient:
            self.pts=self.orient_pts(boundary,0)
        self.pts=[center]+self.pts + [self.pts[0] ]

        self.construct_graph()

class Unfolded():
    """container class for the unfolded objects,
        - used to check whether they fit on a sheet
        - moving the objects around as a single group"""
    def __init__(self, source, boundary, folds_flaps_a=[], folds_flaps_b=[], folds_inner=[], holes=[]):
        self.b_pts=boundary
        self.f_a=folds_flaps_a
        self.f_b=folds_flaps_b
        self.f_i=folds_inner
        self.holes=holes

        self.source=source

        self.opt_a=0.0

    def optimize(self, opt_type="width", iterations=10, panel_dimensions=(100000.0, 100000.0) ):

        width_angle,length_angle,area_angle,data=optimal_rec(
            self.boundary, iterations, panel_dimensions[0], panel_dimensions[1]
        )

        best_width=data[width_angle]["width"]
        best_length=data[length_angle]["length"]
        best_area=data[area_angle]["area"]

        if opt_type=="width":
            self.opt_a=width_angle
        elif opt_type=="length":
            self.opt_a=length_angle
        else: # opt type == "area"
            self.opt_a=area_angle

        optimal_width=data[self.opt_a]["width"]
        optimal_length=data[self.opt_a]["length"]
        optimal_area=data[self.opt_a]["area"]

        self.Transform(rg.Transform.Rotation(self.opt_a, centroid(self.b_pts) ) )

        str_list=[]
        for key, items in data.items():
            str_list.append("for angle {}: \n  width: {}\n  length: {}\n  area: {}".format(key, items["width"], items["length"], items["area"]) )
    
        all_data='\n'.join(str_list)

        return self.opt_a, optimal_width, optimal_length, optimal_area, all_data

    def move_to_origin(self):
        self.move_to_position(-centroid(self.b_pts) )

    def move_to_position(self, pt):
        self.Transform(rg.Transform.Translation(pt) )

    def Transform(self, t_matrix):
        transform_objs(self.b_pts, t_matrix)
        transform_objs(self.f_a, t_matrix)
        transform_objs(self.f_b, t_matrix)
        transform_objs(self.f_i, t_matrix)
        transform_objs(self.holes, t_matrix)

    def outline_crv(self):
        return rg.PolyCurve(self.b_pts + self.b_pts[0])

    def rhino_objects(self):
        return self.outline_crv(), self.f_a, self.f_b, self.f_i