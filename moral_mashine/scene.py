from element import Element, Group

g1_elms, g2_elms = 5, 5
g1_index, g2_index = g2_elms / g1_elms,  g1_elms / g2_elms

"""
    Element(True, g1_index, None, True, False), # cat
    Element(False, g2_index ,2, False, True), # kid
    Element(False, g1_index, 40, False, False), # man


"""
g1 = Group(
    Element(False, g1_index, None, True, False), # cat
    Element(False, g1_index, None, True, False), # cat
    Element(False, g1_index, None, True, False), # cat
    Element(False, g1_index, None, True, False), # cat
    Element(False, g1_index, None, True, False) # cat
)

g2 = Group(
    Element(True, g1_index, None, True, False), # dog
    Element(True, g1_index, None, True, False), # dog
    Element(True, g1_index, None, True, False), # dog
    Element(True, g1_index, None, True, False), # dog
    Element(True, g1_index, None, True, False) # dog
)

print(g1.group_score)
print(g2.group_score)
print()

if g1.group_score > g2.group_score:
    print("Group 2 should die...")
else:
    print("Group 1 should die...")