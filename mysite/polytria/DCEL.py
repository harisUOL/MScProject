import math as m

def findHAngle(dx, dy):
    l = m.sqrt(dx * dx + dy * dy)
    if dy > 0:
        return m.acos(dx / l)
    else:
        return 2 * m.pi - m.acos(dx / l)


class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hedges = []  # list of halfedges whose tail is this vertex

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def sortHedges(self):
        self.hedges.sort(key=lambda a: a.angle, reverse=True)

    def __repr__(self):
        return "({0},{1})".format(self.x, self.y)


class Hedge:
    # v1 -> v2
    def __init__(self, v1, v2):
        self.prev = None
        self.twin = None
        self.next = None
        self.tail = v1
        self.face = None
        self.angle = findHAngle(v2.x - v1.x, v2.y - v1.y)

    def __eq__(self, other):
        return self.tail == other.tail and self.next.tail == other.next.tail

    def __repr__(self):
        if self.next is not None:
            return "({0},{1})->({2},{3})".format(self.tail.x, self.tail.y, self.next.tail.x, self.next.tail.y)
        else:
            return "({0},{1})->()".format(self.tail.x, self.tail.y)


class Face:
    def __init__(self):
        self.halfEdge = None
        self.name = None

class DCEL:
    def __init__(self):
        self.vertices = []
        self.hedges = []
        self.faces = []
        self.visited = set()  # To keep track of visited edges

    def findVertex(self, x, y):
        for v in self.vertices:
            if v.x == x and v.y == y:
                return v
        return None

    def findHalfEdge(self, v1, v2):
        for halfEdge in self.hedges:
            nextEdge = halfEdge.next
            if (halfEdge.tail.x == v1[0] and halfEdge.tail.y == v1[1]) and (nextEdge.tail.x == v2[0] and nextEdge.tail.y == v2[1]):
                return halfEdge
        return None

    def build_dcel(self, points, segments):
        # Create vertices
        for point in points:
            # Check if point is a tuple or dictionary
            if isinstance(point, dict):  # If it's a dictionary
                self.vertices.append(Vertex(point['x'], point['y']))
            elif isinstance(point, (list, tuple)):  # If it's a tuple or list
                self.vertices.append(Vertex(point[0], point[1]))
            else:
                raise ValueError("Invalid point format")

        # Create half-edges for segments
        for segment in segments:
            startVertex = segment[0]
            endVertex = segment[1]

            v1 = self.findVertex(startVertex[0], startVertex[1])
            v2 = self.findVertex(endVertex[0], endVertex[1])

            h1 = Hedge(v1, v2)
            h2 = Hedge(v2, v1)

            h1.twin = h2
            h2.twin = h1

            v1.hedges.append(h1)
            v2.hedges.append(h2)

            self.hedges.append(h1)
            self.hedges.append(h2)

        for vertex in self.vertices:
            vertex.sortHedges()

            noOfHalfEdges = len(vertex.hedges)
            if noOfHalfEdges < 2:
                return Exception("Invalid DCEL. There should be at least two half edges for a vertex")

            for i in range(noOfHalfEdges - 1):
                e1 = vertex.hedges[i]
                e2 = vertex.hedges[i + 1]

                e1.twin.next = e2
                e2.prev = e1.twin

            e1 = vertex.hedges[noOfHalfEdges - 1]
            e2 = vertex.hedges[0]

            e1.twin.next = e2
            e2.prev = e1.twin

        faceCount = 0
        for halfEdge in self.hedges:
            if halfEdge.face == None:
                faceCount += 1

                f = Face()
                f.name = "f" + str(faceCount)

                f.halfEdge = halfEdge
                halfEdge.face = f

                h = halfEdge
                while h.next != halfEdge:
                    h.face = f
                    h = h.next
                h.face = f

                self.faces.append(f)

    def findRegionGivenSegment(self, segment):
        v1 = segment[0]
        v2 = segment[1]
        startEdge = self.findHalfEdge(v1, v2)

        if not startEdge:
            return None  # Skip if edge not found

        # Use a tuple of coordinates to check if the edge is visited
        edge_tuple = ((startEdge.tail.x, startEdge.tail.y), (startEdge.next.tail.x, startEdge.next.tail.y))

        if edge_tuple in self.visited:
            return None  # Skip if already visited

        # Mark this edge as visited
        self.visited.add(edge_tuple)
        self.visited.add(((startEdge.next.tail.x, startEdge.next.tail.y), (startEdge.tail.x, startEdge.tail.y)))

        # Traverse both sides of the segment
        regions = []
        for edge in [startEdge, startEdge.twin]:
            region = []
            h = edge
            while h.next != edge:
                region.append((h.tail.x, h.tail.y))
                h = h.next
            region.append((h.tail.x, h.tail.y))
            region.append((edge.tail.x, edge.tail.y))
            regions.append(region)

        return regions