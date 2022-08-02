#     ___                     _ __   _         _            
#    / __|     _ _   __ _    | '_ \ | |_      (_)    __ __  
#   | (_ |    | '_| / _` |   | .__/ | ' \     | |    \ \ /  
#    \___|   _|_|_  \__,_|   |_|__  |_||_|   _|_|_   /_\_\  
#   _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
#   "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
#
#
#   graph.py
#
#   last update 30/07/22
#
#   laurent vouriot
# 
#   The graph data structure to keep the drawn graph in memory.

class Vertex(object):
    """
    Vertex class. 

    On the canvas a vertex is a superposition of a circle item and 
    a text item, the vertex class is used to gather all these items
    in a single object.

    a vertex is thus composed of : 
    - the oval id 
    - the text id 
    - the label
    - the coords 
    - the color
    """
    def __init__(self, oval_id, text_id, label, coords, color=None):
        """
        :param oval_id: (int) id of the vertex circle on the canvas. 
        :param text_id: (int) id of the text label on the canvas.
        :param label: (str) label of the vertex.
        :param coords: (list(int)) coords of the oval on the canvas.
        :param color: (hex) color of the vertex on the canvas, None if 
        not colored.

        Construsctor.
        """
        self.oval_id = oval_id
        self.text_id = text_id
        self.label = label
        self.coords = coords
        self.color = color

    def get_oval(self):
        """
        :returns: (int) oval_id.
        """
        return self.oval_id
    
    def get_text(self):
        """
        :returns: (int) text_id.
        """
        return self.text_id

    def get_label(self):
        """
        :returns: (str) label.
        """
        return self.label

    def get_coords(self): 
        """
        :returns: (list(int)) coords. 
        """
        return self.coords

    def get_color(self):
        """
        :returns: (hex) color.
        """
        return self.color
    
    def get_vertex(self):
        """
        :returns: (Tuple(int, int, str) (oval_id, text_id, label).
        """
        return (self.oval_id, self.text_id, self.label, self.color)

    def set_label(self, new_label):
        """
        :param new_label: (str) Sets the vertex label. 
        """
        self.label = new_label

    def set_oval_id(self, oval_id):
        """
        :param oval_id: (int) Sets the oval_id.
        """
        self.oval_id = oval_id

    def set_label_id(self, label_id):
        """
        :param label_id: (int) Set the label_id.
        """
        self.label_id = label_id
    
    def set_coords (self, coords):
        """
        :param coords: (list(int)) Sets the coords.
        """
        self.coords = coords
    
    def set_color(self, color):
        """
        :param color: (hex) Sets the color.
        """
        self.color = color

    def __repr__(self):
        return 'vertex ({}), color : ({})'.format(self.label, self.color)

# -----------------------------------------------------------------------------

class Edge(object):
    """
    Edge class

    An edge on the canvas is a line with maybe a weight between two verticies
    instances.

    An edge object is composed of : 
    - the start vertex
    - the end vertex
    - the line id 
    - the weight
    - the weight id
    - the color
    """
    def __init__(self, vx_start, vx_end, line_id, weight=None, weight_id=None, color=None):
        """
        :param vx_start: (Vertex) origin vertex of the edge.
        :param vx_end: (Vertex) end vertex of the edge.
        :param line_id: (int) id of the canvas line.
        :param weight: (int) weight the edge.
        :param weight_id: (int) id of the weight text on the canvas.

        Constructor.
        """
        self.vx_start = vx_start
        self.vx_end = vx_end
        self.line_id = line_id
        self.weight = weight
        self.weight_id = weight_id
        self.color = color

    def get_vx_start(self):
        """
        :returns: (Vertex) start vertex of the edge.
        """
        return self.vx_start

    def get_vx_end(self): 
        """
        :returns: (Vertex) end vertex of the edge.
        """
        return self.vx_end

    def get_line_id(self):
        """
        :returns: (int) id of the canvas line i.e the edge.
        """
        return self.line_id

    def get_weight(self):
        """
        :returns: (int) return the weight of the edge.
        """
        return self.weight

    def get_color(self):
        """
        :returns: (hex) return the color of the edge.
        """
        return self.color

    def get_edge(self): 
        """
        :returns: (Tuple(Vertex, Vertex, int)) (start, end, line_id).
        """
        return (self.vx_start, self.vx_end, self.line_id)

    def set_line_id(self, line_id):
        """
        :param line_id: (int) Sets the id of the line.
        """
        self.line_id = line_id

    def set_weight_id(self, weight_id):
        """
        :param weight_id: (int) Sets the weight_id.
        """
        self.weight_id = weight_id

    def set_color(self, color): 
        """
        :param color: (hex) Sets the color.
        """
        self.color = color

    def __repr__(self): 
        """
        repr.
        """
        return 'edge ({},{}), weight : {}, color : {}'.format(self.vx_start,
                                                            self.vx_end,
                                                            self.weight,
                                                            self.color)

# -----------------------------------------------------------------------------

class Graph(object): 
    """
    The Graph class 

    The graph datastructure, to store the drawn graph.
    To simplify the the relation between the graph on the canvas and 
    the actual graph there is an array for the verticies and the edges, 
    and also an adjacency list.

    A graph object can be created in two cases : 
    - an empty graph when we start a new embedding
    - create graph from a serialized object previously drawn.
    """
    def __init__(self, verticies=None, edges=None, directed=False, weighted=False):
        """
        :param verticies: (list(Vertex)) array of verticies. 
        :param edges: (list(Edge)) array of edges.
        :param adjacency_list: (dict) adjacency list.

        Constructor.
        """
        self.directed = directed
        self.weighted = weighted
        
        # empty graph, new drawing
        if verticies == None:
            self.vx_counter = 0
            self.verticies = []
            self.edges = []
        # serialized graph
        else:
            # we retrieve the label on the last vertex
            self.vx_counter = len(verticies) - 1
            self.verticies = verticies
            self.edges = edges

        self.adjacency_list = {}
        self.incidence_matrix = [[]]

    def generate_adjacency_list(self):
        """
        TODO doc
        """
        for vertex in self.verticies:
            self.adjacency_list[vertex.get_label()] = []
        
        for edge in self.edges:
            vx_start_label = edge.get_vx_start().get_label()
            vx_end_label = edge.get_vx_end().get_label()
            edge_weight = edge.get_weight()

            self.adjacency_list[vx_start_label].append((vx_end_label, 
                                                        edge_weight))

            if not self.directed:
                self.adjacency_list[vx_end_label].append((vx_start_label,
                                                          edge_weight))
            print(self.adjacency_list)

    def genereate_incidence_matrix(self):
        """
        TODO doc 
        """
        # resizing the matrix n*n 
        n = len(self.verticies) 
        self.incidence_matrix = [[0] * n for i in range(n)]
        
        for edge in self.edges:
            # we retrieve the indexes of the start/end verticies of the edges
            # because their label can be anything 
            index_vx_start = self.verticies.index(edge.get_vx_start()) 
            index_vx_end = self.verticies.index(edge.get_vx_end())
            
            if self.is_weighted():
                value = edge.get_weight()
            else: 
                value = 1

            self.incidence_matrix[index_vx_start][index_vx_end] = value 
            if not self.directed:
                self.incidence_matrix[index_vx_end][index_vx_start] = value

            print(self.incidence_matrix)

    def find_vx_from_id(self, vx_id):
        """
        :param vx_id: (int) id of the canvas circle 

        :returns: (Vertex) Vertex instance corresponding to the circle id.

        On the canvas when selecting a vertex we get items ids, this 
        function returns the Vertex instance with this circle id.
        """
        for vertex in self.verticies:
            if vx_id == vertex.get_oval():
                return vertex

    def find_edge_from_id(self, line_id):
        """
        :param line_id: (int) id of the canvas line

        :returns: (Edge) Edge instance corresponding to the circle id.

        On the canvas when selecting an edge we get the line id, this 
        function returns the Edge instance corresponding the line id.
        """
        for edge in self.edges:
            if line_id == edge.get_line_id():
                return edge 
    
    def add_vx(self, vertex):
        """
        :param vertex: (Vertex) 

        Add a vertex instance to the datastructure.
        """
        self.verticies.append(vertex)
            
    def add_edge(self, edge):
        """
        :param edge: (Edge) 

        Add an edge instance to the datastructure.
        """
        self.edges.append(edge)

    def delete_vx(self, vx_id):
        """
        :params vx_id: (int) id of the circle item on the canvas

        finds the vertex instance corresponding the circle id and 
        removes it from the datastruture.
        """
        vx = self.find_vx_from_id(vx_id)
        self.verticies.remove(vx)
        
        # removing the incident edges of this vx
        for edge in self.edges:
            if edge.get_vx_start().get_oval() == vx_id or edge.get_vx_end().get_oval() == vx_id:
                self.edges.remove(edge)

    def delete_edge(self, line_id):
        """
        :param line_id: (int) id of the line item on the canvas.

        finds the edge instance corresponding the line id and 
        removes it from the datastruture.
        """
        edge = self.find_edge_from_id(line_id)

        # the edge may be already deleted if we delete its incident vx
        if edge != None:
            self.edges.remove(edge)
        
    def update_vx_color(self, vx_id, color):
        """
        :param vx_id: (int)
        :param color: (hex)

        at first a vertex has no color, when the user color a vertex
        we need to update the color of the vertex instance in the 
        graph instance. 
        """
        vx = self.find_vx_from_id(vx_id)
        vx.set_color(color)
    
    def update_edge_color(self, edge_id, color):
        """
        :param vx_id: (int)
        :param color: (hex)

        edge analogue of update_vx_color. 
        """
        edge = self.find_edge_from_id(edge_id) 
        edge.set_color(color)
        
    def get_and_update_vx_counter(self): 
        """
        convinient method to return the current vertex label
        and increment it.
        """
        tmp = self.vx_counter
        self.vx_counter += 1
        return str(tmp)

    def display_adjacency(self, adjacency_list):
        """
        print the adjacency list for debug. 
        """
        print(adjacency_list)
        for vertex in adjacency_list:
            print(vertex.get_label(), ' : ', 
                    [i for i in adjacency_list[vertex.get_label()]])
            print('------------')

    def get_verticies(self):
        """
        :returns: (list(Vertex)) 
        """
        return self.verticies

    def get_edges(self):
        """
        :returns: (list(Edges))
        """
        return self.edges
    
    def get_adjacency(self):
        """
        :returns: (dict)
        """
        return self.adjacency_list
    
    def set_to_directed(self):
        """
        Set the graph to directed.

        At first all graphs are considered as undirected, but if the user
        add a directed edge the must be set to directed.
        """
        self.directed = True

    def set_to_weighted(self): 
        self.weighted = True

    def is_directed(self):
        return self.directed

    def is_weighted(self):
        return self.weighted

    def __repr__(self): 
        """
        repr.
        """
        string = ''
        for vx in self.verticies:
            string += repr(vx) + '\n'
        for edge in self.edges:
            string += repr(edge) + '\n'
        return string
