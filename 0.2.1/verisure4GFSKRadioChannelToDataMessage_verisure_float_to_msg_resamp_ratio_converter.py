"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, decimation=1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name=' Verisure Float to Msg Resamp Ratio Converter',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=None
        )

        self.message_port_register_out(pmt.intern('msg_out')) # output message port definition

        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.decimation = decimation

    def work(self, input_items, output_items):
        
        paramDictionary = pmt.make_dict()
        paramDictionary = pmt.dict_add(paramDictionary, pmt.intern("resamp_ratio"),  pmt.from_double(float(input_items[0][0])/self.decimation)) 
        self.message_port_pub(pmt.intern('msg_out'), paramDictionary) # publishes PDU to subscriber blocks. args: port, message

        return len(input_items[0])
