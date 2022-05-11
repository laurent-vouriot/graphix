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
#   last update 27/03/22
#
#   laurent vouriot
# 
#   reader parser classes to save and open graphs

import json

from graph import *

class IO(object):
    def find_vx_from_label(self, verticies, vx_label):
        """
        :param vx_id: (int) id of the canvas circle 

        :returns: (Vertex) Vertex instance corresponding to the circle id.

        On the canvas when selecting a vertex we get items ids, this 
        function returns the Vertex instance with this circle id.
        """
        for vertex in verticies:
            if vx_label == vertex.get_label():
                return vertex

    def exist_edge(self, vx_start, vx_end, edges):
        for edge in edges:
            if edge.get_vx_start() == vx_end and edge.get_vx_end() == vx_start:
                return True
        return False

    def read(self, filename):
        with open(filename) as f:
            data = json.load(f)       

        item_counter = 0
        adjacency_list = {}  
        verticies = []
        edges = [] 
        
        for vertex in data['verticies']:
            current_vx = Vertex(item_counter, item_counter+1, vertex['label'], vertex['coords'])
            verticies.append(current_vx)
            adjacency_list[current_vx] = [] 
        
        for vertex in data['verticies']: 
            current_vx = self.find_vx_from_label(verticies, vertex['label'])
            for neighbour in vertex['neighbours']:
                neighbour_vx = self.find_vx_from_label(verticies, neighbour[0])

                if not self.exist_edge(current_vx, neighbour_vx, edges):
                    edges.append(Edge(current_vx, neighbour_vx, item_counter+1, weight=neighbour[1]))
                    item_counter += 1

                adjacency_list[current_vx].append((neighbour_vx, neighbour[1]))
        
        return Graph(verticies, edges, adjacency_list)
    
    def parse(self, filename, graph):
        graph_dict = {}
        graph_dict['directed'] = False
        graph_dict['verticies'] = []
        
        adjacency_list = graph.get_adjacency()
        for vertex in adjacency_list:
            vx_neighbours = [] 
            for elem in adjacency_list[vertex]:
                vx_neighbours.append((elem[0].get_label(), elem[1]))
            vx_data = {'label' : vertex.get_label(), 'coords' : vertex.get_coords(),
                       'neighbours' : vx_neighbours} 

            graph_dict['verticies'].append(vx_data)

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


