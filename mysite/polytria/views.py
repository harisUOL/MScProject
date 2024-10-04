from django.shortcuts import render
from django.http import JsonResponse
import json
import polytria.Regularisation
import polytria.SweepLineAlgorithm
import polytria.DCEL
import polytria.Triangulation

def home(request):
    return render(request, 'polytria/home.html')

def about(request):
    return render(request, 'polytria/about.html')

def regularise_and_triangulate(request):
    if request.method == 'POST':
        coordinates = json.loads(request.body)
        
        tri_coordinates = [(coord['x'], coord['y']) for coord in coordinates]
         
        # coonversion for easier handling
        tri_trimmed_coordinates = [{'X': round(coord[0], 1), 'Y': round(coord[1], 1)} for coord in tri_coordinates]

        # edges based on the order of the points provided 
        tri_edges = []
        for i in range(len(tri_trimmed_coordinates) - 1):
            start = tri_trimmed_coordinates[i]
            end = tri_trimmed_coordinates[i + 1]
            tri_edge = polytria.SweepLineAlgorithm.Edge(start, end)
            tri_edges.append(tri_edge)
            
        tri_edges.append(polytria.SweepLineAlgorithm.Edge(tri_trimmed_coordinates[-1], tri_trimmed_coordinates[0]))

        # priority queue instance
        tri_pq = polytria.SweepLineAlgorithm.classify_vertices(tri_trimmed_coordinates)

        # classifying vertex types
        tri_classified_vertices = []
        while not tri_pq.is_empty():
            tri_vertex = tri_pq.pop()
            tri_classified_vertices.append(tri_vertex)
        
        # regulrised diagonals 
        tri_diagonals = polytria.Regularisation.find_diagonals(tri_classified_vertices)
        
        if not tri_diagonals:
            # directly triangulating polygon when no regularisation is necessary
            combined_diagonals = polytria.Triangulation.triangulate_monotone_polygon(tri_coordinates)
        else:
            segments = []
            for edge in tri_edges:
                segments.append([(edge.start['X'], edge.start['Y']), (edge.end['X'], edge.end['Y'])])

            for diagonal in tri_diagonals:
                segments.append([(diagonal['source']['X'], diagonal['source']['Y']),
                                 (diagonal['end']['X'], diagonal['end']['Y'])])

            myDCEL = polytria.DCEL.DCEL()
            myDCEL.build_dcel(tri_coordinates, segments)

            # monotone regions
            all_regions = []
            for diagonal in tri_diagonals:
                regions = myDCEL.findRegionGivenSegment(
                    [(diagonal['source']['X'], diagonal['source']['Y']),
                     (diagonal['end']['X'], diagonal['end']['Y'])]
                )
                if regions:
                    all_regions.extend(regions)

            combined_diagonals = []

            # triangulating each monotone polygon
            for polygon in all_regions:
                triangulated_diagonals = polytria.Triangulation.triangulate_monotone_polygon(polygon)
                combined_diagonals.extend(triangulated_diagonals)
        
        # for easier json parsing
        converted_diagonals = []
        for start, end in combined_diagonals:
            converted_diagonals.append({
                'source': {'X': start[0], 'Y': start[1]},
                'end': {'X': end[0], 'Y': end[1]}
            })
        
        request.session['edges'] = [{'start': edge.start, 'end': edge.end} for edge in tri_edges]
        request.session['diagonals'] = [{'source': diag['source'], 'end': diag['end']} for diag in tri_diagonals]
        request.session['vertices'] = tri_classified_vertices
        request.session['tri_coordinates'] = tri_coordinates
        request.session['converted_diagonals'] = converted_diagonals

        return JsonResponse({'redirect': True})

    edges = request.session.get('edges', [])
    diagonals = request.session.get('diagonals', [])
    vertices = request.session.get('vertices', [])
    tri_coordinates = request.session.get('tri_coordinates', [])
    converted_diagonals = request.session.get('converted_diagonals', [])
    
    # rendering regularise and triangulate.html page 
    return render(request, 'polytria/regularise_and_triangulate.html', {
        'edges': json.dumps(edges),
        'diagonals': json.dumps(diagonals),
        'vertices': json.dumps(vertices),
        'tri_coordinates': json.dumps(tri_coordinates),
        'converted_diagonals': json.dumps(converted_diagonals)
    })
