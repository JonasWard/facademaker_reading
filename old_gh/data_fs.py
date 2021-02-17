from triangle import Triangle
from square import Square
from pyramid import Pyramid

def three_pts(pts, correction_val, side_interlock, mesh_cor_val = False, show_with_cor_val = True):
    tri = Triangle(pts, correction_val, side_interlock, mesh_cor_val)
    x, y, z, u = tri.unfolded()
    vis_2d = [x] + y + z + u
    vis_mesh = tri.mesh(show_with_cor_val)
    unfolded_dict = [tri.bake()]

    return vis_2d, vis_mesh, unfolded_dict

def four_pts(pts, correction_val, side_interlock, split_idx = 0, mesh_cor_val = False, folds = True, show_with_cor_val = True):
    sqr = Square(pts, correction_val, side_interlock, split_idx, mesh_cor_val, folds)
    x, y, z, u = sqr.unfolded()
    vis_2d = [x] + y + z + u
    vis_mesh = sqr.mesh(show_with_cor_val)
    unfolded_dict = [sqr.bake()]

    return vis_2d, vis_mesh, unfolded_dict

def four_pts_c_pt(pts, c_pt, correction_val, side_interlock, mesh_cor_val = False, show_with_cor_val = True):
    pyr = Pyramid(pts, c_pt, correction_val, side_interlock, 0, mesh_cor_val)
    x, y, z, u = pyr.unfolded()
    vis_2d = x + y + z + u
    vis_mesh = pyr.mesh(show_with_cor_val)
    unfolded_dict = [pyr.bake()]

    return vis_2d, vis_mesh, unfolded_dict