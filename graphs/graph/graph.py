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
#   last update 05/05/22
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

    a vertex is thus composed of the oval_id, text_id and the actual 
    label of the vertex.
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

# -----------------------------------------------------------------------------

class Edge(object):
    """
    Edge class

    An edge on the canvas is a line with maybe a weight between two verticies
    instances.
    """
    def __init__(self, vx_start, vx_end, line_id, weight=None, weight_id=None):
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
        :returns: (int) return the weight of the weight.
        """
        return self.weight

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
    def __init__(self, verticies=None, edges=None, adjacency_list=None):
        """
        :param verticies: (list(Vertex)) array of verticies. 
        :param edges: (list(Edge)) array of edges.
        :param adjacency_list: (dict) adjacency list.

        Constructor.
        """
        # empty graph, new drawing
        if adjacency_list == None:
            self.vx_counter = 0
            self.adjacency_list = {}
            self.verticies = []
            self.edges = []
        # serialized graph
        else:
            # we retrieve the label on the last vertex
            self.vx_counter = len(verticies) - 1
            self.adjacency_list = adjacency_list
            self.verticies = verticies
            self.edges = edges
    
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
        self.adjacency_list[vertex] = []
        self.display_adjacency()
            
    def add_edge(self, edge):
        """
        :param edge: (Edge) 

        Add an edge instance to the datastructure.
        """
        self.edges.append(edge)
        vx_start = edge.get_vx_start()
        vx_end = edge.get_vx_end()
        weight = edge.get_weight() 
            
        # for an undirected graph the verticies of an edge are symetrical. <--------- FAUX
        if vx_start != vx_end:
            self.adjacency_list[vx_start].append((vx_end, weight))
            self.adjacency_list[vx_end].append((vx_start, weight))
        else: # loop case
            self.adjacency_list[vx_start].append((vx_end, weight))

        self.display_adjacency()

    def delete_vx(self, vx_id):
        """
        :params vx_id: (int) id of the circle item on the canvas

        finds the vertex instance corresponding the circle id and 
        removes it from the datastruture.
        """
        vx = self.find_vx_from_id(vx_id)
        self.verticies.remove(vx)

        self.adjacency_list.pop(vx)
        
        # removing the incident edges of this vx
        for vertex, neighbour in self.adjacency_list.items():
            for elem in neighbour:
                if vx in elem:
                    self.adjacency_list[vertex].remove(elem)
            self.display_adjacency()

    def delete_edge(self, line_id):
        """
        :param line_id: (int) id of the line item on the canvas.

        finds the vertex instance corresponding the circle id and 
        removes it from the datastruture.
        """
        edge = self.find_edge_from_id(line_id)
        
        self.edges.remove(edge)
        
        vx_start = edge.get_vx_start() 
        vx_end = edge.get_vx_end()
        weight = edge.get_weight()
        
        # if we have delete a vertex connected to an edge
        # the vertex would already be deleted. 
        if vx_start != vx_end:
            pass
            # undirected graph
            # self.adjacency_list[vx_start].remove((vx_end, weight))
            # self.adjacency_list[vx_end].remove((vx_start, weight))
        else: # loop case
            self.adjacency_list[vx_start].remove((vx_start, weight))
        
        self.display_adjacency()

    def update_vx_color(self, vx_id, color):
        vx = self.find_vx_from_id(vx_id)
        vx.set_color(color)


    def get_and_update_vx_counter(self): 
        """
        convinient method to return the current vertex label
        and increment it.
        """
        tmp = self.vx_counter
        self.vx_counter += 1
        return str(tmp)

    def display_adjacency(self):
        """
        print the adjacency list for debug. 
        """
        for vertex in self.adjacency_list:
            print(vertex.get_label(), ' ',
                    [(i[0].get_label(), i[1]) for i  in self.adjacency_list[vertex]])
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

