#     ___                     _ __   _         _            
#    / __|     _ _   __ _    | '_ \ | |_      (_)    __ __  
#   | (_ |    | '_| / _` |   | .__/ | ' \     | |    \ \ /  
#    \___|   _|_|_  \__,_|   |_|__  |_||_|   _|_|_   /_\_\  
#   _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
#   "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
#
#
#   log.py
# 
#   last update 25/03/22
#
#   laurent vouriot

class Log(object):
    """
    Log class
    print logs in the text widget on the app.
    """

    def __init__(self, text):
        """
        :param text: (tk.Text) text widget
        
        constructor.
        """
        self.text = text
        self.line_counter = 0
    
    def log(self, exc=False, **kwargs):
        """
        :param **kwargs: variadic positional arguments  
        
        insert into the text widget the logging data.
        """
        if exc:
            self.text.tag_add('EXC', str(self.line_counter) + '.0', str(self.line_counter) + '.5')
            self.text.tag_config('EXC', foreground='red')
            for key, value in kwargs.items():
                self.text.insert('end', value + '\n')
        else:
            for key, value in kwargs.items():
                self.text.insert('end', '[LOG] {} : {}\n'.format(key, value))

        self.line_counter += 1
