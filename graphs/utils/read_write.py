#     ___                     _ __   _         _            
#    / __|     _ _   __ _    | '_ \ | |_      (_)    __ __  
#   | (_ |    | '_| / _` |   | .__/ | ' \     | |    \ \ /  
#    \___|   _|_|_  \__,_|   |_|__  |_||_|   _|_|_   /_\_\  
#   _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
#   "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
#
#
#   reader_parser.py
#
#   last update 30/07/22
#
#   laurent vouriot
# 
#   reader parser classes to save and open graphs

import json

from graph.graph import *

class IO(object):
    def find_vx_from_label(self, verticies, vx_label):
        """
        :param vx_id: (int) id of the canvas circle.

        :returns: (Vertex) Vertex instance corresponding to the circle id.

        On the canvas when selecting a vertex we get items ids, this 
        function returns the Vertex instance with this circle id.
        """
        for vertex in verticies:
            if vx_label == vertex.get_label():
                return vertex

    def exist_edge(self, vx_start, vx_end, edges):
        """
        :param vx_start: (Vertex) start vertex.
        :param vx_end: (Vertex) end vertex.
        :param edges: (list(Edge)) List of edges.

        Given a start and end verticies check in the edge list
        wether this edge really exists.
        """
        for edge in edges:
            if edge.get_vx_start() == vx_end and edge.get_vx_end() == vx_start:
                return True
        return False

    def read(self, filename):
        """
        :param filename: (str) file where the graph is saved.

        open a .graph file and read its content and construct a graph.
        """
        with open(filename) as f:
            data = json.load(f)       

        item_counter = 0
        verticies = []
        edges = [] 
            
        directed = data['directed']
        weighted = data['weighted']

        # read verticies
        for vertex in data['verticies']:
            current_vx = Vertex(item_counter, 
                                item_counter+1, 
                                vertex['label'], 
                                vertex['coords'], 
                                color=vertex['color'])

            verticies.append(current_vx)
         
        # read edges
        for edge in data['edges']:
            vx_start = None
            vx_end = None

            for vx in verticies:
                if edge['vx_start'] == vx.get_label():
                    vx_start = vx 
                if edge['vx_end'] == vx.get_label():
                    vx_end = vx
            
            current_edge = Edge(vx_start,
                                vx_end,
                                edge['line_id'],
                                weight=edge['weight'],
                                color=edge['color'])

            edges.append(current_edge) 

        return Graph(verticies=verticies, 
                     edges=edges, 
                     directed=directed,
                     weighted=weighted) 
    
    def parse(self, filename, graph):
        """
        :param filename: (str) file where to save the save.
        :param graph: (Graph) Graph instance we want to save.
        """
        graph_dict = {}
        graph_dict['directed'] = graph.is_directed()
        graph_dict['weighted'] = graph.is_weighted()
        graph_dict['verticies'] = []
        graph_dict['edges'] = []
        
        for vertex in graph.get_verticies():
            vx_data = {
                       'label' : vertex.get_label(),
                       'coords' : vertex.get_coords(),
                       'color' : vertex.get_color()
                      }
            graph_dict['verticies'].append(vx_data)

        for edge in graph.get_edges():
            edge_data = {
                          'vx_start' : edge.get_vx_start().get_label(), 
                          'vx_end' : edge.get_vx_end().get_label(), 
                          'line_id' : edge.get_line_id(),
                          'weight' : edge.get_weight(),
                          'color' : edge.get_color()
                         }   

            graph_dict['edges'].append(edge_data)
        
        json.dump(graph_dict, filename, indent=2) 

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    io = IO()
    graph = Graph()

    vx1 = Vertex(1, 1, '1', [1, 2])
    vx2 = Vertex(2, 2, '2', [3, 3])
    vx3 = Vertex(3, 3, '3', [1, 3])

    e1 = Edge(vx1, vx2, 4) 
    e2 = Edge(vx1, vx3, 5)


    graph.add_vx(vx1)
    graph.add_vx(vx2)
    graph.add_vx(vx3)

    graph.add_edge(e1) 
    graph.add_edge(e2) 

    print(io.read('ex.graph').get_edges())


