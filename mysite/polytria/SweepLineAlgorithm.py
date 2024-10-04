import heapq
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f"[{self.start}, {self.end}]"
    
class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, vertex):
        # Negative y for max-heap, if y's are equal, compare x's (smaller x gets priority)
        heapq.heappush(self.queue, (-vertex['Y'], vertex['X'], vertex))

    def pop(self):
        return heapq.heappop(self.queue)[2]  # Return the vertex (removing the y and x)

    def is_empty(self):
        return len(self.queue) == 0
 
def angle_between_points(p1, p2, p3):
    v1 = (p1['X'] - p2['X'], p1['Y'] - p2['Y'])
    v2 = (p3['X'] - p2['X'], p3['Y'] - p2['Y'])
    angle = math.atan2(v2[1], v2[0]) - math.atan2(v1[1], v1[0])
    angle = angle + 2 * math.pi if angle < 0 else angle 
    return angle

def classify_vertex(v, prev, next):
    # interior angle at v
    interior_angle = angle_between_points(prev, v, next)
    
    # seperating vertices based on whether they are greater than pi or not
    if prev['Y'] < v['Y'] > next['Y']:
        if interior_angle < math.pi:  
            return "SPLIT"
        else:  
            return "START"
    elif prev['Y'] > v['Y'] < next['Y']:    
        if interior_angle < math.pi: 
            return "MERGE"
        else: 
            return "END"
    else:
        return "REGULAR"

            
# classifing vertices by priority quewue
def classify_vertices(coordinates):
    
    pq = PriorityQueue()
    n = len(coordinates)

    for i in range(n):
        prev = coordinates[i - 1]
        curr = coordinates[i]
        next = coordinates[(i + 1) % n]

        vertex_type = classify_vertex(curr, prev, next)
        curr['type'] = vertex_type

        pq.push(curr)

    return pq
