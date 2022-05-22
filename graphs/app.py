#     ___                     _ __   _         _            
#    / __|     _ _   __ _    | '_ \ | |_      (_)    __ __  
#   | (_ |    | '_| / _` |   | .__/ | ' \     | |    \ \ /  
#    \___|   _|_|_  \__,_|   |_|__  |_||_|   _|_|_   /_\_\  
#   _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
#   "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
#
#
#   app.py
# 
#   last update 04/05/22
#
#   laurent vouriot
#
#   The main app file where the window and 
#   the widgets are created.

from tkinter import filedialog as fd
from tkinter import PhotoImage  # app icon 
from tkinter import ttk
from tkinter.colorchooser import askcolor 

from PIL import ImageGrab # save as png

import time

from ui.items import *
from utils.log import * 
from utils.read_write import * 
from utils.graph_exc import *

class App(tk.Frame):
    """
    App class 

    derived from tk.Frame. 

    Contains instanciate the widgets and the graph datastructure.
    """
    def __init__(self, master=None):
        """
        :param master: (tk.Frame) 
        Constructor.
        """
        self.graph = Graph()
        tk.Frame.__init__(self, master)
        self.configure(bg='#D7FDF0')
        self.grid(sticky='nsew')
        self.createWidgets()

    def createWidgets(self):
        """
        Set up : 
        - the window
        - the menu bar 
        - the canvas 
        - the text log area 
        - the buttons to draw the items
        """
        # window resize
        top=self.winfo_toplevel()                
        top.rowconfigure(0, weight=1)            
        top.columnconfigure(0, weight=1)         
        self.rowconfigure(0, weight=1)           
        self.columnconfigure(1, weight=1)

        # menu 
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar)
        self.file_menu.add_command(label='New', command=self.new)
        self.file_menu.add_command(label='Open', command=self.open)
        self.file_menu.add_command(label='Save', command=self.save)
        self.file_menu.add_command(label='Export', command=self.export)

        self.menubar.add_cascade(label='File', menu=self.file_menu) 

        # canvas
        self.canvas = CanvasWidget(self)
        self.canvas.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        # text
        self.text = tk.Text(self, height=10, bg='#D7FDF0')
        self.text.grid(row=2, column=1, sticky=tk.N+tk.S+tk.E+tk.W) 
        self.text.see('end')

        # buttons
        self.create_buttons()
        
        # log
        self.text_log = Log(self.text)
    
    def create_buttons(self):      
        """
        Create a frame and the buttons to draw the items.
        """
        # Frame for buttons
        button_frame = tk.Frame(self, bg='#D7FDF0')
        button_frame.grid(row=0, column=0, sticky='ns')
        
        # vertex 
        self.vertex = tk.Button(button_frame, text='Vertex',
                                command=self.useVertexDrawer,
                                bg='#D7FDF0', activebackground='#B2FFD6')
        
        self.vertex.grid(row=1, column=0, sticky='new')

        # edge
        self.edge = tk.Button(button_frame, text='Edge', 
                              command=self.useEdgeDrawer, 
                              bg='#D7FDF0', activebackground='#B2FFD6')
        self.edge.grid(row=2, column=0, sticky='new') 

        # directed edge
        self.directed_edge = tk.Button(button_frame, text='Directed edge', 
                                       command=self.useDirectedEdgeDrawer, 
                                       bg='#D7FDF0', activebackground='#B2FFD6')
        self.directed_edge.grid(row=3, column=0, sticky='new') 


        # select
        self.select = tk.Button(button_frame, text='Select', 
                                command=self.select,
                                bg='#D7FDF0', activebackground='#B2FFD6')
        self.select.grid(row=4, column=0, sticky='new')
        
        # rubber 
        self.rubber = tk.Button(button_frame, text='Rubber', 
                                command=self.useRubber,
                                bg='#D7FDF0', activebackground='#B2FFD6')
        self.rubber.grid(row=5, column=0, sticky='new')
        
        
        # color selector
        self.color_selector = tk.Button(button_frame, text='Color', 
                               command=self.select_color, 
                               bg='#D7FDF0', activebackground='#B2FFD6')
        self.color_selector.grid(row=6, column=0, sticky='new') 


    def new(self):
        """
        New graph drawing, reset the canvas the datastructure and
        the text log.
        """
        self.canvas.delete('all')
        self.text.delete('1.0', 'end')
        del self.graph
        self.graph = Graph()

    def open(self):
        """
        Open a .graph file and draw it on the canvas.
        """
        filetypes = (('Graph files', '*.graph'),)

        filename = fd.askopenfilename(title='Open a file',
                                      initialdir='../saved',
                                      filetypes=filetypes)

        reader = IO()
        self.graph = reader.read(filename)
        self.drawGraph()

    def save(self):
        """
        Save a drawn graph as .graph file
        """
        parser = IO()
        file_name = fd.asksaveasfile(initialfile='graph.graph',
                                     defaultextension='.graph',
                                     filetypes=(('Graph files', '*.graph'),), 
                                     mode='w')
        
        if file_name is None:
            return

        parser.parse(file_name, self.graph)

    def export(self):
        """
        Save drawn graph as png. 
        """
        file_name = fd.asksaveasfilename(initialfile='img.png',
                                         defaultextension='.png',
                                         filetypes=(('png file', '*.png'),))
        if file_name is '': 
            return
        # we have to wait otherwise the dialogue box would still
        # displayed on the picture
        time.sleep(0.5)

        ImageGrab.grab(bbox=(
            self.canvas.winfo_rootx(),
            self.canvas.winfo_rooty(),
            self.canvas.winfo_rootx() + self.canvas.winfo_width(),
            self.canvas.winfo_rooty() + self.canvas.winfo_height()
        )).save(file_name)

    
    def drawGraph(self):
        """
        when .graph file is opened first the the datastructure is 
        created from the .graph file. From the new made Graph instance 
        we will draw it on the canvas.
        """
        self.canvas.delete('all')
        self.graph.display_adjacency()

        r = 10
        for vertex in self.graph.get_verticies():
            x = vertex.get_coords()[0] 
            y = vertex.get_coords()[1] 
                
            oval_id = self.canvas.create_oval(x-r, y-r, x+r, y+r, tag='ovals')
            label_id = self.canvas.create_text(x,
                                               y, 
                                               text=vertex.get_label(), 
                                               tag='labels')
            vertex.set_oval_id(oval_id)
            vertex.set_label_id(label_id)

        for edge in self.graph.get_edges():
            x_start = edge.get_vx_start().get_coords()[0]
            y_start = edge.get_vx_start().get_coords()[1]
            x_end = edge.get_vx_end().get_coords()[0]
            y_end = edge.get_vx_end().get_coords()[1]

            #TODO ARROW 
            # if the edge is a loop
            if x_start == x_end and y_start == y_end:
                line_id = self.canvas.create_oval(x_start-25, y_start-25,
                                                  x_start+15, y_start+15,
                                                  tag='loops')

                weight_id = self.canvas.create_text(x_start, y_start-25,
                                                    text=edge.get_weight(),
                                                    tag='loop_weights')
            # common edge
            else:
                x_center = (x_end + x_start) / 2
                y_center = (y_end + y_start) / 2
            
                line_id = self.canvas.create_line(x_start, y_start,
                                                  x_end, y_end,
                                                  tag='lines')

                weight_id = self.canvas.create_text(x_center, y_center,
                                                    text=edge.get_weight(),
                                                    tag='weights')
            
            # when opened the .graph file contains canvas ids of the items from 
            # the previous drawing, but when redrawn, the ids won't en the same
            # that's why we set them again.
            edge.set_line_id(line_id)
            edge.set_weight_id(weight_id)
        
    # on the canvas most of the drawing is made with the left clic
    # is used most of the time. So each time we select an item 
    # we need to unbind left clic from the previous item and bind
    # it again to the current item.
    def select(self):
        """
        Bind left clic to the select item. 
        """
        self.canvas.unbind('<Button-1>')
        self.canvas.bind('<Button-1>', Select(self.canvas,
                                              self.text_log,
                                              self.graph))

    def useVertexDrawer(self):
        """
        Bind left clic to the vertex item. 
        """
        self.canvas.unbind('<Button-1>')
        self.canvas.bind('<Button-1>', DrawVertex(self.canvas,
                                                  self.text_log,    
                                                  self.graph))
        
    def useEdgeDrawer(self):
        """
        Bind left clic to the edge item.
        """
        self.canvas.unbind('<Button-1>')
        self.canvas.bind('<Button-1>', DrawEdge(self.canvas, 
                                                self.text_log, 
                                                self.graph))

    def useDirectedEdgeDrawer(self):
        """
        Bind left clic to the the edge item with directed.
        """
        self.canvas.unbind('<Button-1>')
        self.canvas.bind('<Button-1>', DrawEdge(self.canvas,
                                                self.text_log,
                                                self.graph, 
                                                directed=True))
    def useRubber(self):
        """
        Bind left clic to the rubber item.
        """
        self.canvas.unbind('<Button-1>')
        self.canvas.bind('<Button-1>', DeleteItem(self.canvas,
                                                  self.text_log,
                                                  self.graph))

    def select_color(self):
        color = askcolor(title="Color selector")
        self.canvas.unbind('<Button-1>')
        self.canvas.bind('<Button-1>', ColorItem(self.canvas, 
                                                 self.text_log,
                                                 self.graph,
                                                 color))


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    master = tk.Tk()
    master.title('graphix')
    master.geometry('1000x700')
    
    # icon, need to be multiplateform
    # photo = PhotoImage(file = '../src/petersen_icon.png')
    # master.iconphoto(False, photo)

    app = App(master)
    app.mainloop()
