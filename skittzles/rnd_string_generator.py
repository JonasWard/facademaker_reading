import random
from base_conversions import baseconvert

def generate_rnd_values(x_dim, y_dim, base):
    base_range = 2 ** base
    string_set = []
    ori_strings = []
    for i in range(y_dim):
        string = ''
        for j in range(x_dim):
            string += str( random.randint(0, base_range - 1) )

        ori_string = string
        string = int(string, base_range)

        string_set.append(baseconvert(string, 36))
        ori_strings.append(ori_string)
    
    return 'ftypo' + str(base) + '=' + '_'.join(string_set), '_'.join(ori_strings)

if __name__ == "__main__":
    examples = [
        [6, 5, 1],
        [5, 7, 2],
        [2, 10, 2],
        [8, 2, 2],
        [8, 9, 3],
        [6, 8, 3]
    ]
    
    this_file = open("ftypos.csv", 'a')
    other_file = open("ref.csv", 'a')

    ftypos, refs = [], []
    
    for x, y, b in examples:
        f_typo, ref = generate_rnd_values(x, y, b)
        ftypos.append(f_typo)
        refs.append(ref)

    
    this_file.write('\n'.join( ftypos ) )
    other_file.write('\n'.join( refs ) )
    this_file.close()
    other_file.close()