#     ___                     _ __   _         _            
#    / __|     _ _   __ _    | '_ \ | |_      (_)    __ __  
#   | (_ |    | '_| / _` |   | .__/ | ' \     | |    \ \ /  
#    \___|   _|_|_  \__,_|   |_|__  |_||_|   _|_|_   /_\_\  
#   _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
#   "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
#
#
#   exc.py
# 
#   last update 06/04/22
#
#   laurent vouriot
#
#   graphix exceptions

class GraphError(Exception): 
    def __init__(self, message, text_log):
        self._message = '[EXC] ' + message
        text_log.log(exc=True, msg=self._message)
    
    def __str__(self):
        return self._message
