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

    def __init__(self, 
        c=3.00e8,
        distance_to_target_m=100.0 * 1.0e3,
        target_vel_mps=100.0 * 1.0e3,
        lambda_m=2,
        pri_sec=1.0/3.0e3,
        samp_rate=4e6
    ):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Target Injection',   # will show up in GRC
            in_sig=[(np.complex64,1333*18)],
            out_sig=[(np.complex64,1333*18)]
        )
        
        self.log = gr.logger(self.alias())
        
        # set class member variables by input arguments
        self.c = c
        self.distance_to_target_m = distance_to_target_m        
        self.target_vel_mps = target_vel_mps
        self.lambda_m = lambda_m
        self.pri_sec = pri_sec
        self.samp_rate = samp_rate
        
        # calculate range bin and doppler shift of target
        self.num_samples_to_target = self.distance_to_target_m * self.samp_rate / self.c

        self.doppler_shift_hz = 2 * self.target_vel_mps / self.lambda_m
        
        
        

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        self.log.info(f"length of vector: {len(input_items[0])}")
        output_items[0][:] = input_items[0] * 1
        return len(output_items[0])
