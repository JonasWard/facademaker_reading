# pattern generation

p_b_set={
    "flat" : [["straight", "straight"]],
    "clockwise" : [["positive", "positive"]],
    "counter_clockwise" : [["negative", "negative"]],
    "alternating_A" : [["negative", "positive"], ["positive", "negative"]],
    "alternating_B" : [["positive", "negative"], ["negative", "positive"]],
    "flaps" : ["flap"],
    "easyFix_A" : [["easyfix_neg", "easyfix_pos"], ["easyfix_pos", "easyfix_neg"]],
    "easyFix_B" : [["easyfix_pos", "easyfix_neg"], ["easyfix_neg", "easyfix_pos"]]
}

inverted_patterns=[
    "alternating_A",
    "alternating_B",
    "easyFix_A",
    "easyFix_B"
]

def invert_pattern(value):
    if value=="positive":
        return "negative"
    elif value=="negative":
        return "positive"
    elif value=="easyfix_pos":
        return "easyfix_neg"
    elif value=="easyfix_neg":
        return "easyfix_pos"

def filling_pattern(p_name, cnt = 4, fix = True):
    global p_b_set

    full_pattern_list=[p_b_set[p_name][i%len(p_b_set[p_name])][:] for i in range(cnt)]

    if (p_name in inverted_patterns) and fix:
        full_pattern_list[0][0]=full_pattern_list[-1][-1]

    return full_pattern_list

def simple_pattern_parser(name="flat", cnt=4):
    return filling_pattern(name, cnt)

def pyramid_pattern_parser(name="flat", cnt=4):
    global p_b_set

    pentagon_set=filling_pattern(name, cnt-1, fix=False)
    if (p_name in inverted_patterns):
        triangle_set=[[invert_pattern(v) for v in ([pentagon_set[0][0], pentagon_set[-1][-1]])]]
    else:
        triangle_set=[[pentagon_set[0][0], pentagon_set[-1][-1]]]
    triangle_set=p_b_set["flaps"]+p_b_set["flaps"]+triangle_set
    pentagon_set=p_b_set["flaps"]+pentagon_set+p_b_set["flaps"]

    return pentagon_set, triangle_set

def cube_group_pattern_parser(name="flat", cnts=(4, 4)):
    return [simple_pattern_parser(name, cnts[0]) for i in range(cnts[1])]