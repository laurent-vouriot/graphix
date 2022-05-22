<!--
	 ___                     _ __   _         _            
    / __|     _ _   __ _    | '_ \ | |_      (_)    __ __  
   | (_ |    | '_| / _` |   | .__/ | ' \     | |    \ \ /  
    \___|   _|_|_  \__,_|   |_|__  |_||_|   _|_|_   /_\_\  
   _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
   "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
-->
-------------------------------------------------------------
# Graphix 
## Python GUI to draw __graphs__ !

-------------------------------------------------------------
running in __python3__. 

### Right now you can : 

- Draw simple graphs : 
![pertersen_graph](src/petersen_demo.png)
- Draw directed and weighted graphs :   
![weighted_graph](src/weighted_graph_demo.png)

- Save the graph you are working on
- Export the Graph in .png

### Libraries needed :
- Tkinter
- PIL 

to install them run : 
```
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade tk
python3 -m pip install --upgrade Pillow
```

to run the program :

```
python3 /graphix/graphs/app.py
```
### Future work : 
- Implements algorithms (Shortest path, Spanning tree, Djikstra...).
- Compatible with windows.
- Export to tikz for Latex.

