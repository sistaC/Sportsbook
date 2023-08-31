def find_internal_nodes_num(tree):
    counter = {}
    for ix, item in enumerate(my_tree):
        if item != ix and item != -1:
            counter[item] = counter.get(item,0) + 1
    return len(counter)


my_tree = [4, 4, 1, 5, -1, 4, 5]
print(find_internal_nodes_num(my_tree))