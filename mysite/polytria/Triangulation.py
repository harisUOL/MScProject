def angle_between(p1, p2, p3):
    v1 = (p2[0] - p1[0], p2[1] - p1[1])
    v2 = (p3[0] - p1[0], p3[1] - p1[1])
    
    cross_product = v1[0] * v2[1] - v1[1] * v2[0]
    
    # angle is < 180 degrees means cross product is positive
    return cross_product > 0

def on_different_chains(vertex1, vertex2, left_chain, right_chain):
    return (vertex1 in left_chain and vertex2 in right_chain) or (vertex1 in right_chain and vertex2 in left_chain)

# chain identification based on the y-monotone polygon
def identify_chains(vertices):
    
    sorted_vertices = sorted(vertices, key=lambda v: (-v[1], v[0]))
     
    top_vertex = sorted_vertices[0]
    bottom_vertex = sorted_vertices[-1]
    
    left_chain = [top_vertex]
    right_chain = [top_vertex]
    
    top_index = vertices.index(top_vertex)
    bottom_index = vertices.index(bottom_vertex)
    
    # traversing from top to bottom 
    if top_index < bottom_index:
        left_chain += vertices[top_index + 1 : bottom_index + 1]
        right_chain += vertices[:top_index + 1][::-1] + vertices[bottom_index + 1:][::-1]
    else:
        right_chain += vertices[bottom_index : top_index][::-1]
        left_chain += vertices[top_index + 1:] + vertices[:bottom_index + 1]
    
    return left_chain, right_chain

def identify_polygon_edges(vertices):
    
    polygon_edges = set()
    n = len(vertices)
    for i in range(n):
        polygon_edges.add((vertices[i], vertices[(i+1) % n]))
        polygon_edges.add((vertices[(i+1) % n], vertices[i]))
    return polygon_edges

# function to triangulate the monotone polygons
def triangulate_monotone_polygon(vertices):
    
    left_chain, right_chain = identify_chains(vertices)

    polygon_edges = identify_polygon_edges(vertices)

    stack = []
    diagonals = []

    sorted_vertices = sorted(set(vertices), key=lambda v: (-v[1], v[0]))
    stack.append(sorted_vertices[0])
    stack.append(sorted_vertices[1])

    for i in range(2, len(sorted_vertices)):
        
        current_vertex = sorted_vertices[i]
        
        # if vertices are on different chains
        if on_different_chains(current_vertex, stack[-1], left_chain, right_chain):
            
            # pop all vertices from stack adding diagonals to each popped vertex except the last
            while len(stack) > 1:
                top_vertex = stack.pop()
                if (top_vertex, current_vertex) not in polygon_edges and top_vertex != current_vertex: 
                    diagonals.append((top_vertex, current_vertex))
            
            stack.append(sorted_vertices[i-1])
            stack.append(current_vertex)
            
        else:
            
            top_vertex = stack.pop()
            while len(stack) > 0:
                second_top_vertex = stack.pop()
                if angle_between(current_vertex, top_vertex, second_top_vertex):
                    if (current_vertex, second_top_vertex) not in polygon_edges and current_vertex != second_top_vertex: 
                        diagonals.append((current_vertex, second_top_vertex))
                    top_vertex = second_top_vertex
                else:
                    stack.append(second_top_vertex)
                    break
            
            stack.append(top_vertex)
            stack.append(current_vertex)

    last_vertex = sorted_vertices[-1]
    while len(stack) > 1:
        top_vertex = stack.pop()
        if (top_vertex, last_vertex) not in polygon_edges and top_vertex != last_vertex: 
            diagonals.append((top_vertex, last_vertex))

    return diagonals
