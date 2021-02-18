FUNCTION_TYPES={
    'd2': 'square',             # normal square
    'q1lift': 'square',         # square with a lifted side
    'd4': 'pyramid',            # pyramid
    'q4': 'quad_group',         # group of four quads
    't1': 'triangle',           # isosceles triangle
    't2': 'triangle',           # rightangle triangle
    't3': 'diamond',            # 2 triangles grouped side by side
    't4': 'square',             # with shift
}

FUNCTION_SHIFT_VALUES={
    'd2': 0.,
    'q1lift': 0.,
    'd4': 0.,
    'q4': 0.,
    't1': .5,
    't2': 0.,
    't3': 0.,
    't4': .5,
}

HORIZONTAL_COUNT_MULTIPLIER={
    'd2': 1,
    'q1lift': 1,
    'd4': 1,
    'q4': 1,
    't1': 2,
    't2': 2,
    't3': 1,
    't4': 1,
}

DEFAULT_DICT={
    'ft': 't2',                                     # function type, defining the complexity and which objects to use
    'fgh': 7,                                       # amount of panels in horizontal direction
    'fgv': 5,                                       # amount of panels in vertical direction
    'frat': 1.395,                                  # proportion of the leght and height of the panel elements
    'ftypo2': '1h9u1h_1h9u1h_1h9u1h_1h9u1h_1h9u1h', # for reference, not present if only an ftypo 2 is given
    'ftypo': [                                      # obj mask used for the facade
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    'mirrh': True,                                  # whether the point set is mirrored horizontally (heights + fold)
    'mirrv': True,                                  # whether the point set is mirrored vertically   (heights + fold)
    'konh': True,                                   # whether the direction of the fold is switched horizontally (pyramid: inside / outside, square: different diagonal)
    'konv': True,                                   # whether the direction of the fold is switched vertically   (pyramid: inside / outside, square: different diagonal)
    'roth': 0,                                      # whether the point set is rotated horizontally (heights + fold)
    'rotv': 0,                                      # whether the point set is rotated vertically   (heights + fold)
    'fp': 0,                                        # ???
    'c00': 0.0,                                     # bottom left corner height
    'c01': 0.0,                                     # top left corner height
    'c10': 0.69999999999999996,                     # bottom right corner height
    # 'c11': 0.0,                                     # top right corner height
    'hs': [0.0, 0.0, 0.69999999999999996],          # list of all heights, clockwise
    'mat': '',                                      # material tag - not used
}

DEFAULT_CONSTRUCTION_PARAMETERS={
    "flap_h_max" : 30.,
    "correction_val" : .7,
    "flap_h" : 20.0,
    "flap_w" : 40.0,
    "mesh_correction_val" : False,
    "show_correction_val" : True,
    "fold_idx" : 0,                 # front-end parameter
    "min_pt_height" : 50.,
    "orient" : True,                # legacy parameter
    "pattern" : "flat"              
}
