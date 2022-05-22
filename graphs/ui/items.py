#     ___                     _ __   _         _            
#    / __|     _ _   __ _    | '_ \ | |_      (_)    __ __  
#   | (_ |    | '_| / _` |   | .__/ | ' \     | |    \ \ /  
#    \___|   _|_|_  \__,_|   |_|__  |_||_|   _|_|_   /_\_\  
#   _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
#   "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
#
#
#   items.py
# 
#   last update 01/05/22
#
#   laurent vouriot
#
#   the differents items (vertex, edge...) that can be drawn on the canvas

from tkinter import simpledialog

from math import isclose

from ui.canvasWidget import *
from graph.graph import *
from utils.graph_exc import *  

class BaseItem(object):
    """
    BaseItem class
    to derivate all the others items.
    """
    def __init__(self, canvas, text_log, graph):
        """
        :param canvas: (tk.Canvas) canvas where the items are going to get drawn
        :param text_log: (tk.Text) text widget to print the logs
        :param graph: (Graph) graph data structure 

        constructor.
        """
        self.canvas = canvas
        self.selected_items = None
        self.graph = graph
        self.text_log = text_log

    def __call__(self, event):
        """
        :param event: (tk.event) 
        
        In the application there is a button for each item, that when clicked will 
        bind the left clic button to the object instance. Using the __call__ 
        method helps us to use the item instance as function and do some work on 
        the canvas.
        """
        # there can be multiple items selected when clicked as they can overlap
        # (e.g  a vertex on the canvas is an oval and a text item)
        # so selected_items is a tuple containing one or more items ids.
        self.selected_items = self.canvas.find_overlapping(event.x-10, event.y-10,
                                                           event.x+10, event.y+10)

    def is_vertex(self, item_ids):
        """
        :param item_ids: (Tuple(int)) 

        when we clic on an item (or a superposition of items) we will need to
        check wether its is an edge or a vertex in the graph point of view. 
        """

        # as a drawn vertex on the canvas is an oval and a text item 
        # and sometimes edges, we just check if one of the selected 
        # item is indeed the oval, no need to verify the other items. 
        for vx in self.graph.get_verticies():
            if vx.get_oval() in item_ids:
                return True
        return False

    def is_edge(self, item_ids):
        """
        :param items_ids: (Tuple(int))

        edge analogous of is_vertex().
        """
        for edge in self.graph.get_edges():
            if edge.get_edge()[2] in item_ids:
                return True
        return False

# -----------------------------------------------------------------------------

class Select(BaseItem):
    """
    Select class. 

    Item to move the verticies on the canvas. 
    """
    def __call__(self, event):
        BaseItem.__call__(self, event)

        self.text_log.log(coords=(event.x, event.y))
        self.canvas.bind('<Motion>', self.move)
        self.canvas.bind('<ButtonRelease-1>', self.deselect)
        
    # TODO proper logging doc and comments
    def move(self, event):
        x, y = event.x, event.y
        for item in self.selected_items:
            # move vertex
            if 'ovals' in self.canvas.gettags(item):
                self.canvas.coords(item, x-10, y-10, x+10, y+10)
                self.graph.find_vx_from_id(item).set_coords([x-10, y-10, x+10, y+10])
            # move vx label
            elif 'labels' in self.canvas.gettags(item):
                self.canvas.coords(item, x, y)
            # move edge
            elif 'lines' in self.canvas.gettags(item):
                x_start, y_start, x_end, y_end = self.canvas.coords(item)
                x_center = (x_end + x_start) / 2
                y_center = (y_end + y_start) / 2
                weight = False
                 
                # if there is a weight on the edge
                if 'weights' in self.canvas.gettags(self.canvas.find_closest(x_center, 
                                                                             y_center)):
                    weight_label = self.canvas.find_closest(x_center, y_center)
                    weight = True

                if isclose(x_start, x, abs_tol=50) and isclose(y_start, y, abs_tol=50):
                    self.canvas.coords(item, x, y, x_end, y_end)
                    if weight: 
                        new_x = (x_end + x) / 2
                        new_y = (y_end + y) / 2
                        self.canvas.coords(weight_label, new_x, new_y)
                else: 
                    self.canvas.coords(item, x_start, y_start, x, y)
                    if weight:
                        new_x = (x_start + x) / 2
                        new_y = (y_start + y) / 2
                        self.canvas.coords(weight_label, new_x, new_y)
            
            # loop case
            elif 'loops' in self.canvas.gettags(item):
                self.canvas.coords(item, x-30, y-30, x+5, y+5)
                 
                # if there is a weight on the loop 
                if 'loop_weights' in self.canvas.gettags(
                                       self.canvas.find_closest(x, y-35)):

                    weight_label = self.canvas.find_closest(x, y-35)
                    self.canvas.coords(weight_label, x, y-35)


    def deselect(self, event):
        self.canvas.unbind('<Motion>') 

# -----------------------------------------------------------------------------

class DrawVertex(BaseItem):
    """
    DrawVertex class 
        
    draws a vertex on the canvas. 
    A canvas vertex is the superposition of a circle item and and a text item.
    """
    def __call__(self, event):
        """
        :param event: (tk.Event)

        when the instance is called a vertex will be drawn on the canvas 
        at the selected coords.
        """
        BaseItem.__call__(self, event)
        r = 10   # Blob radius
        
        # we create first the oval (i.e a circle) 
        # and then the text label, thus the text item will always be on top
        # of the the circle item.
        oval_id = self.canvas.create_oval(event.x-r, event.y-r,
                                          event.x+r, event.y+r, tag='ovals')
        
        # if the label is not defined by the user we use counter in the Graph 
        # instance, we keep it in a variable to simplify logging
        label = simpledialog.askstring("Input", "Label (press cancel for no label)",
                                         parent=self.canvas)
        if label is None or label == '':
            label = str(self.graph.get_and_update_vx_counter())

        label_id = self.canvas.create_text(event.x, event.y, text=label, tag='labels')
        
        self.canvas.add_vx_items((oval_id, label_id))

        # after drawing the vertex on the canvas we need to save it in the
        # datastructure. 
        self.graph.add_vx(Vertex(oval_id, label_id, label, self.canvas.coords(oval_id)))

        self.text_log.log(vertex=label)
        self.text_log.log(coords=(event.x, event.y))
        
# -----------------------------------------------------------------------------

class DrawEdge(BaseItem):
    """
    DrawEdge class
    
    draws an edge on the canvas.
    A canvas edge is a line and maybe a text item if the graph is weighted.
    """
    def __init__(self, canvas, text, graph, directed=False):
        """
        :param directed: (bool) if True the graph is directed, else its 
        a simple graph.
            
        Constructor.
        """
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.vx1 = None
        self.vx2 = None
        BaseItem.__init__(self, canvas, text, graph) 
        
        # if the graph is directed the edge will point to the latter selected 
        # vertex.
        if directed:
            self.arrow = tk.LAST
        else:
            self.arrow = ''

    def __call__(self, event):
        """
        :param event: (tk.Event)
        
        When the instance is called an edge will be drawn on the canvas 
        between the two selected verticies.
        """
        BaseItem.__call__(self, event)

        # if its the first vertex we select we the save the coords and return 
        # waiting for the second vertex to be selected.
        if not self.x1 and not self.x2:
            if self.is_vertex(self.selected_items):
                # we use selected_items[0] because the id of the circle is 
                # always the first element in the canvas item list.
                self.vx1 = self.graph.find_vx_from_id(self.selected_items[0])

                # we select [:2] because canvas.coords returns the coords of 
                # the rectangle around the item
                self.x1, self.y1 = self.canvas.coords(self.vx1.get_oval())[:2]

                self.text_log.log(selected_vertex=self.vx1.get_label())
            else:
                raise GraphError('No vertex here', self.text_log) 
            return
        
        if self.is_vertex(self.selected_items):
            self.vx2 = self.graph.find_vx_from_id(self.selected_items[0])
            
            # loop case 
            if self.vx1 == self.vx2:
                self.draw_loop()
                return

            self.x2, self.y2 = self.canvas.coords(self.vx2.get_oval())[:2]
            self.text_log.log(selected_vertex=self.vx2.get_label())
        else:
            raise GraphError('No vertex here', self.text_log) 
        
        # we compute the center of each vertex
        x_start = self.x1+10
        y_start = self.y1+10

        x_end = self.x2+10
        y_end = self.y2+10
        
        x_center = (x_end + x_start) / 2
        y_center = (y_end + y_start) / 2
        
        line_id = self.canvas.create_line(x_start, y_start,
                                          x_end, y_end, 
                                          arrow=self.arrow, tag='lines')
        

        weight = simpledialog.askinteger("Input", 
                                         "Weight ? (press cancel for no weight)",
                                         parent=self.canvas)
        
        weight_id = self.canvas.create_text(x_center,
                                            y_center, 
                                            text=weight,
                                            tag='weights')


        self.graph.add_edge(Edge(self.vx1, self.vx2, line_id,
                                 weight=weight, weight_id=weight_id))

        self.canvas.add_edge_items((line_id, weight_id))

        self.text_log.log(edge_created=(self.vx1.get_label(), self.vx2.get_label()))
        
        # we reset all the coords for the next edge to be drawn. 
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.vx1 = None 
        self.vx2 = None

    def draw_loop(self):
        """
        when we select two times the same vertex to draw an edge, we must draw 
        a loop.
        """
        line_id = self.canvas.create_oval(self.x1-25, self.y1-25,
                                          self.x1+15, self.y1+15, tag='loops')

        weight = simpledialog.askinteger("Input", "Weight ?",
                                         parent=self.canvas)
        
        weight_id = self.canvas.create_text(self.x1, self.y1-25,
                                            text=weight, tag='loop_weights')

        self.graph.add_edge(Edge(self.vx1, self.vx2, line_id, 
                            weight=weight, weight_id=weight_id))

        self.canvas.add_edge_items((line_id, weight_id))

        self.text_log.log(loop_created=(self.vx1.get_label(), self.vx2.get_label()))

        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.vx1 = None 
        self.vx2 = None

# -----------------------------------------------------------------------------

class DeleteItem(BaseItem):
    """
    DeleteItem class
    Removes an item from the canvas and from the graph.
    """
    def __call__(self, event):
        """
        :param event: (tk.Event)
        """
        BaseItem.__call__(self, event)

        for item in self.selected_items:
            if 'ovals' in self.canvas.gettags(item):
                self.graph.delete_vx(item)
            elif 'lines' in self.canvas.gettags(item):
                self.graph.delete_edge(item)
            elif 'loops' in self.canvas.gettags(item):
                self.graph.delete_edge(item)

            self.canvas.delete_item(item)

# -----------------------------------------------------------------------------

class ColorItem(BaseItem):
    def __init__(self, canvas, text_log, graph, color): 
        BaseItem.__init__(self, canvas, text_log, graph)
        self.color = color[1]
        
    def __call__(self, event):
        BaseItem.__call__(self, event)
        for item in self.selected_items:
            # return each time so it colors only one item each time
            if 'ovals' in self.canvas.gettags(item):
                self.canvas.itemconfigure(item, fill=self.color)
                return
            elif 'lines' in self.canvas.gettags(item):
                self.canvas.itemconfigure(item, fill=self.color)
                return
            elif 'loops' in self.canvas.gettags(item):
                self.canvas.itemconfigure(item, fill=self.color)
                return



        

