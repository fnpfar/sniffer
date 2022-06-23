"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, enable_Log=False):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Verisure Tag Counter',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=None              # there is no output stream
        )
        
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.enableLog = enable_Log
        
        self.tagCounter = 0

    def work(self, input_items, output_items):
        
        
        tags = self.get_tags_in_window(0, 0, len(input_items[0])) # gets all tags in current buffer. Params: input, rel. start, rel. end
        for tag in tags:
            self.tagCounter += 1
         
        if self.enableLog and (len(tags) > 0):
            print ('')
            print ('   0. Verisure Tag Counter:')
            print (' .----------------------------------------->')
            print (' | Tag Count:', self.tagCounter)
            print (' *----------------------------------------->')
            print ('')
        return len(input_items[0])
