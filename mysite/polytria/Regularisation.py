import math

def euclidean_distance(p1, p2):
    return math.sqrt((p2['X'] - p1['X']) ** 2 + (p2['Y'] - p1['Y']) ** 2)

def diagonal_exists(diagonals, vertex1, vertex2):
    for diagonal in diagonals:
        if (diagonal['source'] == {'X': vertex1['X'], 'Y': vertex1['Y']} and
            diagonal['end'] == {'X': vertex2['X'], 'Y': vertex2['Y']}) or \
           (diagonal['source'] == {'X': vertex2['X'], 'Y': vertex2['Y']} and
            diagonal['end'] == {'X': vertex1['X'], 'Y': vertex1['Y']}):
            return True
    return False
 
# returning diagonals for monotone polygon
def find_diagonals(vertices):
    diagonals = []

    split_vertices = [v for v in vertices if v['type'] == 'SPLIT']
    merge_vertices = [v for v in vertices if v['type'] == 'MERGE']
    start_vertices = [v for v in vertices if v['type'] == 'START']
    end_vertices = [v for v in vertices if v['type'] == 'END']

    if any(merge['Y'] < split['Y'] for merge in merge_vertices for split in split_vertices) or any(split['Y'] > merge['Y'] for split in split_vertices for merge in merge_vertices):
        # connecting split vertices to satart vertices if no split is found
        for i, vertex in enumerate(split_vertices):
            min_distance = float('inf')
            closest_vertex = None

            for j, start_vertex in enumerate(start_vertices):
                distance = euclidean_distance(vertex, start_vertex)

                # closest start vertex
                if distance < min_distance and start_vertex['Y'] > vertex['Y']:
                    min_distance = distance
                    closest_vertex = start_vertex

            if closest_vertex and not diagonal_exists(diagonals, vertex, closest_vertex):
                diagonals.append({
                    'source': {'X': vertex['X'], 'Y': vertex['Y']},
                    'end': {'X': closest_vertex['X'], 'Y': closest_vertex['Y']}
                })

        # connect merge vertices to end vertices if no merge is found
        for i, vertex in enumerate(merge_vertices):
            min_distance = float('inf')
            closest_vertex = None

            for j, end_vertex in enumerate(end_vertices):
                distance = euclidean_distance(vertex, end_vertex)

                if distance < min_distance and end_vertex['Y'] < vertex['Y']:
                    min_distance = distance
                    closest_vertex = end_vertex

            if closest_vertex and not diagonal_exists(diagonals, vertex, closest_vertex):
                diagonals.append({
                    'source': {'X': vertex['X'], 'Y': vertex['Y']},
                    'end': {'X': closest_vertex['X'], 'Y': closest_vertex['Y']}
                })
        
    else:
        # coonnect all splits to each other 
        for i, vertex in enumerate(split_vertices):
            min_distance = float('inf')
            closest_vertex = None

            for j, other_vertex in enumerate(split_vertices):
                if i == j:
                    continue  # Skip comparison with itself

                distance = euclidean_distance(vertex, other_vertex)

                if distance < min_distance and other_vertex['Y'] > vertex['Y']:
                    min_distance = distance
                    closest_vertex = other_vertex

            if closest_vertex and not diagonal_exists(diagonals, vertex, closest_vertex):
                diagonals.append({
                    'source': {'X': vertex['X'], 'Y': vertex['Y']},
                    'end': {'X': closest_vertex['X'], 'Y': closest_vertex['Y']}
                })

        # connect all mergesto each other 
        for i, vertex in enumerate(merge_vertices):
            min_distance = float('inf')
            closest_vertex = None

            for j, other_vertex in enumerate(merge_vertices):
                if i == j:
                    continue  

                distance = euclidean_distance(vertex, other_vertex)

                if distance < min_distance and other_vertex['Y'] < vertex['Y']:
                    min_distance = distance
                    closest_vertex = other_vertex

            if closest_vertex and not diagonal_exists(diagonals, vertex, closest_vertex):
                diagonals.append({
                    'source': {'X': vertex['X'], 'Y': vertex['Y']},
                    'end': {'X': closest_vertex['X'], 'Y': closest_vertex['Y']}
                })
        

    # connect closest splits to closest merges
    final_split_vertex = None
    final_merge_vertex = None
    min_distance = float('inf')

    for split_vertex in split_vertices:
        for merge_vertex in merge_vertices:
            distance = euclidean_distance(split_vertex, merge_vertex)

            if distance < min_distance:
                min_distance = distance
                final_split_vertex = split_vertex
                final_merge_vertex = merge_vertex

    if final_split_vertex and final_merge_vertex:
        if not diagonal_exists(diagonals, final_split_vertex, final_merge_vertex):
            diagonals.append({
                'source': {'X': final_split_vertex['X'], 'Y': final_split_vertex['Y']},
                'end': {'X': final_merge_vertex['X'], 'Y': final_merge_vertex['Y']}
            })

    return diagonals