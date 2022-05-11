#     ___                     _ __   _         _            
#    / __|     _ _   __ _    | '_ \ | |_      (_)    __ __  
#   | (_ |    | '_| / _` |   | .__/ | ' \     | |    \ \ /  
#    \___|   _|_|_  \__,_|   |_|__  |_||_|   _|_|_   /_\_\  
#   _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
#   "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
#
#
#   canvasWidget.py
# 
#   last update 16/04/22
#
#   laurent vouriot
#
#   canvas wrapper 

import tkinter as tk

class CanvasWidget(tk.Canvas):

    def __init__(self, window):
        tk.Canvas.__init__(self, window)
        self._vx_items = []
        self._edge_items = []

    def add_vx_items(self, vx_items):
        self._vx_items.append(vx_items)
    
    def add_edge_items(self, edge_items):
        self._edge_items.append(edge_items)
    
    def delete_item(self, item_id):
        for items in self._vx_items + self._edge_items:
            if item_id in items: 
                for item in items:
                    self.delete(item)
