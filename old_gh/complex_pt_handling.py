import Rhino.Geometry as rg
import math

arcs=[]

def tangent_normal(pt_0, pt_1, negative=False):
    t=rg.Vector3d(pt_1-pt_0)
    t.Unitize()
    if negative:
        n=rg.Vector3d(-t.Y, t.X, 0.0)
    else:
        n=rg.Vector3d(t.Y, -t.X, 0.0)
    return t, n

def create_half_circle(pt, r, t, n):
    pt_a=rg.Point3d(pt - rg.Point3d(t * r) )
    pt_b=rg.Point3d(pt + rg.Point3d(n * r) )
    pt_c=rg.Point3d(pt + rg.Point3d(t * r) )
    global arcs
    arc_crv=rg.ArcCurve(rg.Arc(pt_a, pt_b, pt_c) )
    arcs.append(arc_crv)
    return arc_crv

def triangulate(pt_0, pt_1, dis_0, dis_1, negative=False):
    t, n = tangent_normal(pt_0, pt_1, negative)

    crv_0=create_half_circle(pt_0, dis_0, t, n)
    crv_1=create_half_circle(pt_1, dis_1, t, n)

    i_s=rg.Intersect.Intersection.CurveCurve(crv_0, crv_1, 0.001, 0.0)
    final_pt=i_s[0].PointA
    # print(final_pt)
    return final_pt

def bounding_rec(pts, angle=None):
    xs, ys = [], []
    
    if angle is None:

        for pt in pts:
            xs.append(pt.X)
            ys.append(pt.Y)

        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)

        return rg.Point3d(x_min, y_min, 0.0), x_max-x_min, y_max-y_min

    else:

        r_tm=rg.Transform.Rotation(angle, rg.Point3d(0,0,0) )
        loc_pts=[rg.Point3d(pt) for pt in pts]
        [pt.Transform(r_tm) for pt in loc_pts]
        return bounding_rec(loc_pts)

def optimal_rec(pts, iterations=50, max_width=10000.0, max_length=10000.0):
    delta=.5*math.pi/(iterations - 1)

    data_dict={}
    for i in range(iterations):
        # duplicate pts
        loc_pts=[rg.Point3d(pt) for pt in pts]
        angle=i*delta
        _, w, l=bounding_rec(loc_pts, angle)
        if w < max_width and l < max_length:
            data_dict[angle]={"width":w,"length":l,"area":w*l}

    print(data_dict)

    if any(data_dict):
        min_width=min(data_dict, key=lambda k: data_dict[k]["width"])
        min_length=min(data_dict, key=lambda k: data_dict[k]["length"])
        min_area=min(data_dict, key=lambda k: data_dict[k]["area"])
        return min_width, min_length, min_area, data_dict

    else:
        return None, None, None, None

def transform_objs(objs, t_m):
    [obj.Transform(t_m) for obj in objs]

def centroid(pts):
    centroid=rg.Point3d(pts[1])
    for pt in pts[1:]:
        centroid+=pt

    centroid*=1.0/float(len(pts) )
    return rg.Point3d(centroid)

class Segment():
    """ segment class, defined by two points ( a line ) two definitions:
        - defined using orignal pts and new unfolded given: simple_side, complex_side
        - defined using only the new unfolded given: simple_flap, portrusion """
    def __init__(self, pt_0, pt_1):
        self.pt_0=pt_0
        self.pt_1=pt_1

    @property
    def t(self):
        _t=rg.Vector3d(self.pt_1-self.pt_0)
        _t.Unitize()

        return _t

    @property 
    def n(self):
        return rg.Vector3d(-self.t.Y, self.t.X, 0.0)

    @property
    def dis00(self):
        return self.pt_0.Z

    @property
    def dis01(self):
        return self.pt_0.DistanceTo(rg.Point3d(self.pt_1.X, self.pt_1.Y, 0.0) )

    @property
    def dis10(self):
        return self.pt_1.DistanceTo(rg.Point3d(self.pt_0.X, self.pt_0.Y, 0.0) )

    @property
    def dis11(self):
        return self.pt_1.Z

    @property
    def dis(self):
        return self.pt_0.DistanceTo(self.pt_1)

    def simple_side(self, pt_0, pt_1):
        pt_0_1=triangulate(pt_0, pt_1, self.dis00, self.dis10, True)
        pt_1_1=triangulate(pt_0, pt_1, self.dis01, self.dis11, True)

        return [pt_0_1, pt_1_1], [rg.Line(pt_0, pt_1)]

    def complex_side(self, pt_0, pt_1, h_max, pattern_type=(0,0) ):
        new_pts, fold_a=self.simple_side(pt_0, pt_1)

        n_s_0=Segment(new_pts[0], pt_0)
        n_s_1=Segment(new_pts[1], pt_1)

        seg_pts=[]
        folds_b=[]

        # n_s_0
        loc_folds_b=[]
        if pattern_type[0] == 0:
            loc_seg_pts=[new_pts[0] ]
        elif pattern_type[0] == 1:
            loc_seg_pts, _ = n_s_0.portrusion(h_max, False)
        else:
            loc_seg_pts, loc_folds_b = n_s_0.portrusion(h_max, True)

        loc_seg_pts.reverse()
        seg_pts.extend(loc_seg_pts)
        folds_b.extend(loc_folds_b)

        # n_s_1
        loc_folds_b=[]
        if pattern_type[1] == 0:
            loc_seg_pts=[new_pts[1] ]
        elif pattern_type[1] == 1:
            loc_seg_pts, loc_folds_b = n_s_1.portrusion(h_max, False)
        else:
            loc_seg_pts, _ = n_s_1.portrusion(h_max, True)

        seg_pts.extend(loc_seg_pts)
        folds_b.extend(loc_folds_b)

        return seg_pts, fold_a, folds_b

    def simple_flap(self, h, w, invert=False):
        iv=-1.0 if invert else 1.0

        mv=rg.Point3d(iv*self.t*w + self.n*h)
        new_pts=[
            self.pt_0+rg.Point3d(iv*self.t*w + self.n*h),
            self.pt_1+rg.Point3d(-iv*self.t*w + self.n*h)
        ]

        fold_lines=[rg.Line(self.pt_0, self.pt_1)]

        return new_pts, fold_lines

    def portrusion(self, h_max, direction):
        # print("creating a portrusion")
        t, n = tangent_normal(self.pt_0, self.pt_1)
        dir_val=1.0 if direction else -1.0

        h=self.dis
        if h < h_max:
            pt_s=[self.pt_0+dir_val*n*h]
        else:
            pt_s=[
                self.pt_0+dir_val*n*h_max,
                self.pt_0+dir_val*n*h_max+t*(h-h_max)
            ]

        return pt_s, [rg.Line(self.pt_0, self.pt_1)]

class Base():
    """ main geometric solution class allowing for a given set of boundary points
    to generate a mesh, unfolding it, adding flaps and calculating the sides, and
    two different methods of incalculating tolerances """
    def projected_pts(self, offset=False):
        """projects the input points onto the bottom surface
        stores those projected point into the class"""
        pts=self.ori_pts if (not(offset) and self.has_offset) else self.pts
        return [rg.Point3d(pt.X, pt.Y, 0.0) for pt in pts]

    def start_run(self):
        self.has_graph=False
        self.has_offset=False
        self.has_holes=False
        self.ori_pts=[]

    @property
    def count(self):
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
        c_pt=centroid(pts)
        pt_copy=[pt-c_pt for pt in pts]

        angles=[math.atan2(pt.Y, pt.X) for pt in pt_copy]
        angles, pts=zip(*sorted(zip(angles, pts) ) )
        
        pts=list(pts)
        # self.pts.reverse()
        return pts[start_idx:]+pts[:start_idx]

    def construct_graph(self):
        # print("a graph with {} vertexes".format(len(self.pts)))

        v_list=[i for i in range(self.count) ]
        v_list.pop(0)
        f_list=[]
        # print(v_list)
        for i in range(self.count - 2):
            v_a=v_list.pop(0)
            f_list.append((0, v_a, v_list[0]))

        self.has_graph=True

        return f_list

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
            pts, loc_folds = Segment(pt_0, pt_1).simple_side(pt_0_new, pt_1_new)
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
                pts, loc_folds_a, loc_folds_b = Segment(pt_0, pt_1).complex_side(
                    pt_0_new,
                    pt_1_new,
                    h_max,
                    pattern_type
                )
            elif isinstance(pattern_type, int):
                if pattern_type==3:
                    pts, loc_folds_a = Segment(pt_0_new, pt_1_new).simple_flap(flap_h, flap_w, False)
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

        self.f_list=self.construct_graph()

class Center(Base):
    def __init__(self, boundary, center, orient=True):
        self.start_run()
        self.pts=boundary
        if orient:
            self.pts=self.orient_pts(self.pts, 0)
        self.pts=[center]+self.pts

        self.f_list=self.construct_graph()

class ClosedPyramid(Base):
    def __init__(self, boundary, center, orient=True):
        self.start_run()
        if orient:
            self.pts=self.orient_pts(boundary,0)
        self.pts=[center]+self.pts + [self.pts[0] ]

        self.f_list=self.construct_graph()

class Pyramid():
    def __init__(self, boundary, center):
        self._count=len(boundary)

        self.bottom_shape=Center(boundary, center, False)
        self.top_triangle=Simple([boundary[0], center, boundary[-1]], False)

    @property
    def count(self):
        return self._count

    def pattern_maker(self, pattern):
        pattern=[(2,2)] if pattern is None else pattern

        return [pattern[i%len(pattern)] for i in range(self.count)]

    def transformation(self, pts, folds_a, folds_b, w_l=(0.0, 0.0) ):
        width_increase=10.0

        crv=rg.PolylineCurve(pts)

        c_pt, w_new, l_new=bounding_rec(pts)
        mv_matrix=rg.Transform.Translation(
            rg.Vector3d(-c_pt + rg.Point3d(w_l[0] + width_increase, w_l[1], 0.0) ) 
        )

        crv.Transform(mv_matrix)
        transform_objs(folds_a, mv_matrix)
        transform_objs(folds_b, mv_matrix)

        return mv_matrix, (w_l[0]+w_new+width_increase,w_l[1]+l_new), crv

    def add_simple_sides(self):
        b_pts, b_folds_a, b_folds_b=self.bottom_shape.add_simple_sides()
        t_pts, t_folds_a, t_folds_b=self.top_triangle.add_simple_sides()

        self.mv_a, w_l, crv_a=self.transformation(b_pts, b_folds_a, b_folds_b)
        self.mv_b, w_l, crv_b=self.transformation(t_pts, t_folds_a, t_folds_b, w_l)
        
        return (crv_a, crv_b), (b_folds_a, t_folds_a), (b_folds_b, t_folds_b)

    def add_complex_sides(self, h_max=10.0, flap_h=20.0, flap_w=40.0, pattern=None):
        pattern=self.pattern_maker(pattern)

        b_pts, b_folds_a, b_folds_b=self.bottom_shape.add_complex_sides(
            h_max, flap_h, flap_w, pattern=pattern[1:]
        )
        t_pts, t_folds_a, t_folds_b=self.top_triangle.add_complex_sides(
            h_max, flap_h, flap_w, pattern=[3,pattern[0],3]
        )

        self.mv_a, w_l, crv_a=self.transformation(b_pts, b_folds_a, b_folds_b)
        self.mv_b, w_l, crv_b=self.transformation(t_pts, t_folds_a, t_folds_b, w_l)
        
        return (crv_a, crv_b), (b_folds_a, t_folds_a), (b_folds_b, t_folds_b)

    def unfolding(self):
        self.bottom_shape.unfolding()
        self.top_triangle.unfolding()

    def polyline_correction(self, value):
        self.bottom_shape.polyline_correction(value)
        self.top_triangle.polyline_correction(value)

    def mesh_correction(self, value):
        self.bottom_shape.mesh_correction(value)
        self.top_triangle.mesh_correction(value)

    def rhino_mesh(self, offset=False):
        return [
            self.bottom_shape.rhino_mesh(offset),
            self.top_triangle.rhino_mesh(offset)
        ]

    def rhino_brep(self, offset=True, brep_offset=False, brep_offset_val=1.0):
        return [
            self.bottom_shape.rhino_brep(offset, brep_offset, brep_offset_val),
            self.top_triangle.rhino_brep(offset, brep_offset, brep_offset_val),
        ]
    def fold_lns(self):
        b_lns, t_lns=self.bottom_shape.fold_lns(), self.top_triangle.fold_lns()

        transform_objs(b_lns, self.mv_a)
        transform_objs(t_lns, self.mv_b)

        return ( b_lns, t_lns )

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
