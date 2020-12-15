from read_link import string_reader, complete_tag_list

f = open("links.csv", 'r')

dicts = []
tag_lists = []

for string in f.readlines():
    dicts.append(string_reader(string) )
    tag_lists.extend(complete_tag_list(string))

print(set(tag_lists) )
print(dicts)

